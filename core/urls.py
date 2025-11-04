from django.contrib import admin
from django.urls import path, include
from clima.views import ClimaBuscarView, TopCiudadesView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ClimaBuscarView.as_view(), name="buscar_ciudad"),
    path("top/", TopCiudadesView.as_view(), name="top_ciudades"),
    path("accounts/", include("accounts.urls")),
]
