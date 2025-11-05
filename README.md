# Clima App (Django)

Mini proyecto web en Django que consulta el clima actual usando la API de Open-Meteo. Incluye autenticación de usuarios (login, logout), vistas con Bootstrap 5 y una vista basada en clases (CBV) para la búsqueda de clima. También incorpora una vista de "Top ciudades" con el clima actual de varias capitales.

## Requisitos

- Python 3.11+
- pip

## Instalación y ejecución en local

1) Crear y activar entorno virtual

   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

2) Instalar dependencias

   ```bash
   pip install django==5.2.7 requests PyJWT
   ```

3) Migraciones y superusuario (opcional, para admin)

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4) Ejecutar servidor

   ```bash
   python manage.py runserver
   ```

## Probar / Rutas

- Inicio: `http://localhost:8000/` — búsqueda de clima (requiere login)
- Top ciudades: `http://localhost:8000/top/` — clima en ciudades populares (requiere login)
- Login (JWT): `http://localhost:8000/accounts/login/`
- Logout: `http://localhost:8000/accounts/logout/`
- Perfil: `http://localhost:8000/accounts/perfil/`
- Secreto: `http://localhost:8000/accounts/secret/` (requiere el permiso `auth.view_user`)

Nota: el registro de usuarios está deshabilitado; ingresa con el superusuario creado.

## Autenticación (JWT)

- Al iniciar sesión se emite un JWT y se guarda en una cookie HttpOnly (`jwt`) con `SameSite=Lax` y `Secure=False` en local.
- El middleware `accounts.middleware.JWTAuthenticationMiddleware` lee el token desde la cookie o desde el encabezado `Authorization: Bearer <token>`, lo valida y adjunta el usuario a `request.user`.
- La duración del token es de 24 horas.

## Estructura

- `core/` — configuración del proyecto (settings, urls)
- `clima/` — app principal (CBV `ClimaBuscarView`, `TopCiudadesView`, formularios, plantillas)
- `accounts/` — login/logout con JWT, perfil y vistas con permisos, middleware y utilidades JWT
- `templates/` — plantillas con herencia desde `clima/base.html`

## Notas

- Se requiere conexión a Internet para consultar Open-Meteo (geocoding y clima actual).
- Panel de administración: `http://localhost:8000/admin/` (si creaste superusuario).

## Autor

Matias Baez

## Licencia

Uso académico.
