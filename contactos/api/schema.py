from pydantic import EmailStr, Field
from ninja import Schema    

class ContactoCreate(Schema):
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    correo: EmailStr
    telefono: str = Field(..., min_length=8)