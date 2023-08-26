from django.urls import path

from .views import dashboard, login_user, logout_user, task

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", login_user, name="login_user"),
    path('logout/', logout_user, name='logout_user'),
    path('task/', task, name='task')
]
