from django.urls import path

from .views import dashboard, login_user

urlpatterns = [
    path("login/", login_user, name="login_user"),
    path("", dashboard, name="dashboard"),
]
