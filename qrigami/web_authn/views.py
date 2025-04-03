"""QRigami. QR code generator site.

Copyright (C) 2025  Andrew Kozmin <syn.kolbasyn.06@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from json import loads

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import FormView, View
from webauthn import generate_registration_options, verify_registration_response
from webauthn.helpers.base64url_to_bytes import base64url_to_bytes
from webauthn.helpers.bytes_to_base64url import bytes_to_base64url

from web_authn.forms import SignInForm, SignUpForm
from web_authn.models import Credentials
from web_authn.serializers import WebAuthnJSONEncoder


class SignUpView(FormView):

    """WebAuthn signup view."""

    template_name = "web_authn/signup.html"
    form_class = SignUpForm


class SignUpStartView(View):

    """WebAuthn signup start view."""

    def post(self, request: HttpRequest) -> JsonResponse:
        """Process post requests."""
        form = SignUpForm(request.POST or None)

        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_json())

        username = form.cleaned_data[User.username.field.name]
        email = form.cleaned_data[User.email.field.name]

        options = generate_registration_options(
            rp_id=settings.HOST,
            rp_name=settings.HOST_NAME,
            user_name=username,
        )

        request.session["challenge"] = bytes_to_base64url(options.challenge)
        request.session["username"] = bytes_to_base64url(username.encode("utf-8"))
        request.session["email"] = bytes_to_base64url(email.encode("utf-8"))

        return JsonResponse(options, WebAuthnJSONEncoder, safe=False)


class SignUpFinishView(View):

    """WebAuthn signup finish view."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Process post requests."""
        challenge = base64url_to_bytes(request.session.pop("challenge"))
        username = base64url_to_bytes(request.session.pop("username")).decode("utf-8")
        email = base64url_to_bytes(request.session.pop("email")).decode("utf-8")

        verified_registration = verify_registration_response(
            credential=loads(request.body.decode("utf-8")),
            expected_challenge=challenge,
            expected_rp_id=settings.HOST,
            expected_origin=settings.ORIGIN,
            require_user_presence=True,
            require_user_verification=True,
        )

        user = User(username=username, email=email, is_active=False)
        user.set_unusable_password()
        user.full_clean()
        user.save()

        credentials = Credentials(
            user=user,
            credential_id=verified_registration.credential_id,
            credential_public_key=verified_registration.credential_public_key,
            sign_count=verified_registration.sign_count,
        )
        credentials.full_clean()
        credentials.save()

        activate_url = reverse(
            "web_authn:activate",
            kwargs={"credential_id": bytes_to_base64url(credentials.credential_id)},
        )
        user.email_user(
            "Email verification",
            f"Verify your email -> click this link: {settings.ORIGIN}{activate_url}",
            fail_silently=False,
        )

        return HttpResponse()


class UserActivationView(View):

    """User activation veiw."""

    def get(self, request: HttpRequest, credential_id: str) -> HttpResponse:
        """Process get requests."""
        credential_id = base64url_to_bytes(credential_id)

        query = (
            User.objects.filter(credentials__credential_id=credential_id)
            .only(User.id.field.name)
        )

        user = get_object_or_404(query)

        user.is_active = True
        user.save(update_fields=[User.is_active.field.name])

        return render(request, "web_authn/email_verification_success.html")


class SignInView(FormView):

    """WebAuthn signin view."""

    template_name = "web_authn/signin.html"
    form_class = SignInForm
