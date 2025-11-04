from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.jwt_login, name="jwt_login"),
    path("logout/", views.jwt_logout, name="jwt_logout"),
    path("perfil/", views.profile, name="profile"),
    path("secret/", views.secret, name="secret"),
]
