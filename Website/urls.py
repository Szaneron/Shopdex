from django.urls import path

from .views import dashboard, login_user, logout_user

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", login_user, name="login_user"),
    path('logout/', logout_user, name='logout_user')
]
