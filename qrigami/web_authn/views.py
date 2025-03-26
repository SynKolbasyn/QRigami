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


from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.views.generic import FormView, View
from webauthn import generate_registration_options

from web_authn.forms import SignUpForm
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
            return HttpResponseBadRequest({"errors": form.errors.as_data()})

        options = generate_registration_options(
            rp_id=settings.HOST,
            rp_name=settings.HOST_NAME,
            user_name=form.cleaned_data[User.username.field.name],
        )
        return JsonResponse(options, WebAuthnJSONEncoder, safe=False)
