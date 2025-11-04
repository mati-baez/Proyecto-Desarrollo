# Clima App (Django)

Mini proyecto web en Django que consulta el clima actual usando la API de Open‑Meteo. Incluye autenticación de usuarios (login, registro, logout), vistas con Bootstrap 5 y una vista basada en clases (CBV) para la búsqueda de clima.

## Requisitos

- Python 3.11+
- pip

## Instalación y ejecución en local

1. Crear y activar entorno virtual

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

2. Instalar dependencias

   ```bash
   pip install django==5.2.7 requests PyJWT
   ```

3. Migraciones y superusuario (opcional, para admin)

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Ejecutar servidor

   ```bash
   python manage.py runserver
   ```

5. Probar

   - Login (JWT): `http://localhost:8000/accounts/login/`
   - Búsqueda de clima (requiere login): `http://localhost:8000/`

   Nota: El login usa JWT almacenado en cookie HttpOnly. El registro está deshabilitado; ingresa con el superusuario.

## Estructura

- `core/` – configuración del proyecto (settings, urls)
- `clima/` – app principal (CBV `ClimaBuscarView`, formulario, plantillas)
- `accounts/` – registro, perfil y vistas con permisos
- `templates/` – plantillas con herencia desde `clima/base.html`

## Autor

Nombre Apellido

## Licencia

Uso académico.
