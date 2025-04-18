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


from django.urls import path

from web_authn.views import (
    SignInFinishView,
    SignInStartView,
    SignInView,
    SignUpFinishView,
    SignUpStartView,
    SignUpView,
    UserActivationView,
)

app_name = "web_authn"

urlpatterns = [
    path(
        "signup/",
        SignUpView.as_view(),
        name="signup",
    ),
    path(
        "signup/start/",
        SignUpStartView.as_view(),
        name="signup_start",
    ),
    path(
        "signup/finish/",
        SignUpFinishView.as_view(),
        name="signup_finish",
    ),
    path(
        "activate/<str:credential_id>/",
        UserActivationView.as_view(),
        name="activate",
    ),
    path(
        "signin/",
        SignInView.as_view(),
        name="signin",
    ),
    path(
        "signin/start/",
        SignInStartView.as_view(),
        name="signin_start",
    ),
    path(
        "signin/finish/",
        SignInFinishView.as_view(),
        name="signin_finish",
    ),
]
