import jwt

from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from .exceptions import TokenExpiredException, IncorrectTokenFormatException


def decode_token(token, public_key, jwt_algorithm) -> dict:
    """
    Decode jwt token and return token payload dictionary.

    Keyword arguments:
        token: jwt token to decode
        public_key: public key used to decode the token
        jwt_algorithm: jwt algorithm used to decode the token
    """
    try:
        payload = jwt.decode(
            token, public_key, jwt_algorithm
        )
        return payload
    except ExpiredSignatureError:
        raise TokenExpiredException
    except InvalidTokenError as e:
        print(e)
        raise IncorrectTokenFormatException
