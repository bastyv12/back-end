# api/auth.py

from ninja import Router
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.errors import HttpError

auth_router = Router()

@auth_router.post("/login")
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if not user:
        raise HttpError(401, "Credenciales inválidas")

    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user_id": user.id,
        "username": user.username
    }
