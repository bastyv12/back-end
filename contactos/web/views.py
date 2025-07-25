from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .forms import ContactoForm
import requests
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout

API_URL = "http://127.0.0.1:8000/api/contactos/"


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)

            # Obtener token JWT desde el backend
            response = requests.post('http://127.0.0.1:8000/api/auth/token/', json={
                 'username': username,
                 'password': password
                 
             })

            if response.status_code == 200:
                token = response.json()['access']
                request.session['token'] = token
                return redirect('lista_contactos')
            else:
                messages.error(request, 'Error al obtener el token JWT')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    print(f"Token guardado en sesión: {token}")


def logout_view(request):
    logout(request)
    request.session.pop('token', None)
    return redirect('login')

# ----------------------------
# Registro de usuario
# ----------------------------
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
        else:
            User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Usuario registrado correctamente. Ahora puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'registration/register.html')


# ----------------------------
# Lista de contactos
# ----------------------------
@login_required
def lista_contactos(request):
    contactos = []
    token = request.session.get('token')
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        contactos = response.json()
    except Exception as e:
        print(f"Error al obtener contactos: {e}")

    return render(request, 'lista_contactos.html', {'contactos': contactos})


# ----------------------------
# Crear contacto
# ----------------------------
@login_required
def crear_contacto(request):
    if request.method == 'POST':
        token = request.session.get('token')
        headers = {'Authorization': f'Bearer {token}'} if token else {}

        data = {
            "nombre": request.POST['nombre'],
            "apellido": request.POST['apellido'],
            "correo": request.POST['correo'],
            "telefono": request.POST['telefono']
        }

        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 201:
            return redirect('lista_contactos')
        else:
            return render(request, 'formulario_contacto.html', {'error': 'Error al guardar contacto'})

    return render(request, 'formulario_contacto.html')


# ----------------------------
# Ver detalle
# ----------------------------
@login_required
def detalle_contacto(request, id):
    token = request.session.get('token')
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    try:
        response = requests.get(f"{API_URL}{id}/", headers=headers)
        response.raise_for_status()
        contacto = response.json()
    except Exception as e:
        contacto = {}
        print(f"Error al obtener detalle: {e}")

    return render(request, 'detalle.html', {"contacto": contacto})


# ----------------------------
# Editar contacto
# ----------------------------
@login_required
def editar_contacto(request, id):
    token = request.session.get('token')
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            response = requests.put(f"{API_URL}{id}/", json=form.cleaned_data, headers=headers)
            if response.status_code == 200:
                return redirect("lista_contactos")
    else:
        try:
            response = requests.get(f"{API_URL}{id}/", headers=headers)
            response.raise_for_status()
            datos = response.json()
            form = ContactoForm(initial=datos)
        except:
            return redirect('lista_contactos')

    return render(request, 'formulario_contacto.html', {"form": form})


# ----------------------------
# Eliminar contacto
# ----------------------------
@login_required
def eliminar_contacto(request, id):
    token = request.session.get('token')
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    try:
        requests.delete(f"{API_URL}{id}/", headers=headers)
    except:
        pass

    return redirect("lista_contactos")
