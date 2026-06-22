from fastapi import HTTPException


class BaseExceptions(Exception):
    detail = "Ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectAlreadyExistsException(BaseExceptions):
    detail = "Объект уже сущетсвует"


class EmailNotRegisteredException(BaseExceptions):
    detail = "Пользователь с таким email не зарегистрирован"


class EmailNotRegisteredHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не зарегистрирован"


class EmailDeletedException(BaseExceptions):
    detail = "Пользователь удален"


class EmailDeletedHTTPException(BaseHTTPException):
    status_code = 403
    detail = "Пользователь удален"


class IncorrectPasswordException(BaseExceptions):
    detail = "Неверный пароль"


class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Неверный email или пароль"


class UserAlreadyExistsException(BaseExceptions):
    detail = "Пользователь уже существует"


class UserEmailAlreadyExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectTokenException(BaseExceptions):
    detail = "Некорректный токен"


class IncorrectTokenHTTPException(BaseHTTPException):
    status_code = 403
    detail = "Некорректный токен"


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class ObjectNotFoundException(BaseExceptions):
    detail = "Объект не найден"


class UserNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class AccessRuleNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Правило не найдено"


class ForbiddenException(BaseExceptions):
    detail = "Недастаточно прав"


class ForbiddenHTTPException(BaseHTTPException):
    status_code = 403
    detail = "Недастаточно прав"
