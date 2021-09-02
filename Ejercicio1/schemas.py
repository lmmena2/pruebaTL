from pydantic import BaseModel

class UserRequestModel(BaseModel):
    valores_cambio: str
    fecha: str

class UserResponseModel(UserRequestModel):
    id: int
