from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, model_name: str, model_id: int):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"{model_name} with ID {model_id} not found."
        

class AlreadyExistsException(HTTPException):
    def __init__(self, model_name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"{model_name} already exists."
        
        
class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Unauthorized access."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = message
