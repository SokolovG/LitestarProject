from litestar.exceptions import HTTPException


class UserAlreadyExistError(HTTPException):
    """User already exist in DB."""
    status_code = 400
    detail = 'User already exist in DB.'

class DatabaseError(Exception):
    """Error with db."""
