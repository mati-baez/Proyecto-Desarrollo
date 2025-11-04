from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, logout as django_logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from .jwt import generate_token, COOKIE_NAME


def signup(request):
    # Registro deshabilitado: redirigir al login JWT
    return redirect("jwt_login")


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


@permission_required("auth.view_user", raise_exception=True)
def secret(request):
    return render(request, "accounts/secret.html")


@csrf_protect
def jwt_login(request):
    # Si ya está autenticado, no mostrar pantalla de login
    if request.method == "GET" and getattr(request, "user", None) and request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL or "/")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "registration/login.html", {"error": "Credenciales inválidas."})

        token = generate_token(user)
        # Asegura que cualquier sesión previa quede cerrada
        try:
            django_logout(request)
        except Exception:
            pass
        response = redirect(settings.LOGIN_REDIRECT_URL or "/")
        # Dev cookie: HttpOnly; Secure=False para entorno local
        response.set_cookie(
            COOKIE_NAME,
            token,
            httponly=True,
            samesite="Lax",
            secure=False,
            path="/",
            max_age=60 * 60 * 24,
        )
        return response

    return render(request, "registration/login.html")


def jwt_logout(request):
    # Cierra sesión basada en sesión si existiera (admin u otras vistas)
    try:
        django_logout(request)
    except Exception:
        pass
    response = redirect("jwt_login")
    # Borra cookie JWT con los mismos atributos usados al crearla
    response.delete_cookie(COOKIE_NAME, path="/", samesite="Lax")
    return response
