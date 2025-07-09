# api/api.py

from ninja import NinjaAPI, Schema
from .models import Contacto
from typing import List
from django.shortcuts import get_object_or_404

api = NinjaAPI(
    title="API Contactos",
    version="1.0",
    docs_url="/docs",  # 👈 habilita Swagger UI
    openapi_url="/openapi.json"  # (opcional, ya está activo)
)
# Esquemas
class ContactoSchema(Schema):
    id: int
    nombre: str
    apellido: str
    correo: str
    telefono: str

class ContactoCreate(Schema):
    nombre: str
    apellido: str
    correo: str
    telefono: str

# Endpoints
@api.get("/contactos/", response=List[ContactoSchema])
def listar_contactos(request):
    return Contacto.objects.filter(active=True)

@api.get("/contactos/{id}/", response=ContactoSchema)
def detalle_contacto(request, id: int):
    contacto = get_object_or_404(Contacto, id=id, active=True)
    return contacto

@api.post("/contactos/", response=ContactoSchema)
def crear_contacto(request, data: ContactoCreate):
    contacto = Contacto.objects.create(**data.dict())
    return contacto

@api.put("/contactos/{id}/", response=ContactoSchema)
def editar_contacto(request, id: int, data: ContactoCreate):
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
    return {"success": True}
