from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# Propiedades compartidas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    role: str = "operator"
    is_active: bool = True


# Schema para creación (recibe password plano)
class UserCreate(UserBase):
    password: str


# Schema para actualizar datos
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    role: str | None = None
    is_active: bool | None = None


# Schema de respuesta pública (NUNCA devuelve password)
class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema para token de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None