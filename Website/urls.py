from django.urls import path

from .views import dashboard, login_user, logout_user, task, task_detail_view, delivery

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", login_user, name="login_user"),
    path('logout/', logout_user, name='logout_user'),
    path('task/', task, name='task'),
    path('task/<int:task_id>/', task_detail_view, name='task_detail_view'),
    path('delivery/', delivery, name='delivery'),
]
