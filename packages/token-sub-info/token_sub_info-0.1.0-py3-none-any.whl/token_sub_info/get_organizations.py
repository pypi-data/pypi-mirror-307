from uuid import UUID

from .decode_token import decode_token
from .exceptions import AllOrganizationAccessForbiddenException


def get_organizations(token, public_key, jwt_algorithm) -> list[UUID]:
    """
    Decode jwt token and return a list of organization UUIDs from token payload dictionary.

    Keyword arguments:
        token: jwt token to decode
        public_key: public key used to decode the token
        jwt_algorithm: jwt algorithm used to decode the token
    """
    payload = decode_token(token, public_key, jwt_algorithm)
    organizations_ids: list[UUID] = payload.get("sub").get("organizations")
    if not organizations_ids:
        raise AllOrganizationAccessForbiddenException
    return organizations_ids
