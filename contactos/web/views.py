from django.shortcuts import render

# Create your views here.
import httpx
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactoForm

API_URL = "http://127.0.0.1:8000/api/v1/contactos/"

@login_required
def lista_contactos(request):
    response = httpx.get(API_URL)
    contactos = response.json()
    return render(request, "lista.html", {"contactos": contactos})

@login_required
def crear_contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            httpx.post(API_URL, json=form.cleaned_data)
            return redirect("lista_contactos")
    else:
        form = ContactoForm()
    return render(request, "formulario.html", {"form": form})

@login_required
def detalle_contacto(request, id):
    contacto = httpx.get(f"{API_URL}{id}/").json()
    return render(request, "detalle.html", {"contacto": contacto})

@login_required
def editar_contacto(request, id):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            httpx.put(f"{API_URL}{id}/", json=form.cleaned_data)
            return redirect("lista_contactos")
    else:
        datos = httpx.get(f"{API_URL}{id}/").json()
        form = ContactoForm(initial=datos)
    return render(request, "formulario.html", {"form": form})

@login_required
def eliminar_contacto(request, id):
    httpx.delete(f"{API_URL}{id}/")
    return redirect("lista_contactos")
