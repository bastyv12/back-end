"""
URL configuration for contactos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.api import api as api_router  # <-- Import correcto
from web import views as web_views
from django.contrib.auth import views as auth_views
from web import views
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout
from web.views import login_view, logout_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_router.urls),  
    path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("", web_views.lista_contactos, name="lista_contactos"),
    path("crear/", web_views.crear_contacto, name="crear_contacto"),
    path("contacto/<int:id>/", web_views.detalle_contacto, name="detalle_contacto"),
    path("editar/<int:id>/", web_views.editar_contacto, name="editar_contacto"),
    path("eliminar/<int:id>/", web_views.eliminar_contacto, name="eliminar_contacto"),
]
