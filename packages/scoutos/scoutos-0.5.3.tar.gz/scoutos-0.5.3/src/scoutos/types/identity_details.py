# This file was auto-generated by Fern from our API Definition.

import typing
from .user_identity import UserIdentity
from .api_key_identity import ApiKeyIdentity

IdentityDetails = typing.Union[UserIdentity, ApiKeyIdentity]
