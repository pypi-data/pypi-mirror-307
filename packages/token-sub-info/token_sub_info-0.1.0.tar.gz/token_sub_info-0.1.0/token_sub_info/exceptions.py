from fastapi import status

from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from .schemas.schemas import ResponseDetail


class ServiceException(HTTPException):
    def __init__(self, status_code=500):
        self.status_code = status_code
        self.detail = jsonable_encoder(
            ResponseDetail(
                code="OTHER_ERROR",
                message="Ошибка взаимодействия с библиотекой token_sub_info."
        )
    )
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectTokenFormatException(ServiceException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)
        self.detail['code'] = "TOKEN_INCORRECT"
        self.detail['message'] = "Неверный формат токена."


class TokenExpiredException(ServiceException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)
        self.detail['code'] = "TOKEN_EXPIRED"
        self.detail['message'] = message="Токен истек."


class AllOrganizationAccessForbiddenException(ServiceException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN)
        self.detail['code'] = "FORBIDDEN"
        self.detail['message'] = "Пользователь не имеет доступа ни к одной из организаций."
