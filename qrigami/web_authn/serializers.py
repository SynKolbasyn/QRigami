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


from django.core.serializers.json import DjangoJSONEncoder
from webauthn import options_to_json
from webauthn.helpers.structs import (
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialRequestOptions,
)


class WebAuthnJSONEncoder(DjangoJSONEncoder):

    """WebAuthn json encoder."""

    def default(self, o: object) -> str:
        """WebAuthn data encoding."""
        if isinstance(
            o,
            (PublicKeyCredentialCreationOptions, PublicKeyCredentialRequestOptions),
        ):
            return options_to_json(o)
        return super().default(o)
