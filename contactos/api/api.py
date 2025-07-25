from ninja import NinjaAPI, Schema
from typing import List
from .models import Contacto
from django.shortcuts import get_object_or_404
from .auth import auth_router
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404
from ninja.errors import ValidationError
from pydantic import EmailStr, Field

# -------------------------
# Autenticación global con JWT
# -------------------------
class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        validated = JWTAuthentication().authenticate(request)
        if validated is None:
            return None
        return validated[0]

# -------------------------
# Instancia de la API
# -------------------------
api = NinjaAPI(
    title="API Contactos",
    version="1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    auth=GlobalAuth()
)

# -------------------------
# Manejadores de errores personalizados
# -------------------------
@api.exception_handler(Http404)
def manejar_404(request, ex):
    return api.create_response(
        request,
        {'detalle': 'No se encontró el recurso solicitado.'},
        status=404
    )

@api.exception_handler(ValidationError)
def manejar_validacion(request, ex):
    return api.create_response(
        request,
        {
            'detalle': 'Error de validación de entrada.',
            'errores': ex.errors
        },
        status=422
    )

# -------------------------
# Esquemas
# -------------------------
class ContactoSchema(Schema):
    id: int
    nombre: str
    apellido: str
    correo: EmailStr
    telefono: str

class ContactoCreate(Schema):
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    correo: EmailStr
    telefono: str = Field(..., min_length=8)

# -------------------------
# Autenticación
# -------------------------
api.add_router("/auth/", auth_router)

# -------------------------
# Endpoints públicos
# -------------------------
@api.get("/contactos/", response=List[ContactoSchema], auth=None)
def listar_contactos(request):
    return Contacto.objects.filter(active=True)

@api.get("/contactos/{id}/", response=ContactoSchema, auth=None)
def detalle_contacto(request, id: int):
    contacto = get_object_or_404(Contacto, id=id, active=True)
    return contacto

# -------------------------
# Endpoints protegidos
# -------------------------
@api.post("/contactos/", response=ContactoSchema)
def crear_contacto(request, data: ContactoCreate):
    contacto = Contacto.objects.create(**data.dict())
    return contacto

@api.put("/contactos/{id}/", response=ContactoSchema)
def actualizar_contacto(request, id: int, data: ContactoCreate):
    contacto = get_object_or_404(Contacto, id=id)
    for attr, value in data.dict().items():
        setattr(contacto, attr, value)
    contacto.save()
    return contacto

@api.delete("/contactos/{id}/")
def eliminar_contacto(request, id: int):
    contacto = get_object_or_404(Contacto, id=id)
    contacto.active = False
    contacto.save()
    return {"success": True, "mensaje": "Contacto eliminado correctamente."}
