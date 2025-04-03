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


from django.contrib.auth.models import User
from django.forms import ModelForm


class SignUpForm(ModelForm):

    """SignUp form class."""

    class Meta:

        """SignUp meta class."""

        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
        )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize form."""
        super().__init__(*args, **kwargs)
        self.fields[User.email.field.name].required = True


class SignInForm(ModelForm):

    """SignIn form class."""

    class Meta:

        """SignIn meta class."""

        model = User
        fields = (
            User.username.field.name,
        )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize form."""
        super().__init__(*args, **kwargs)
