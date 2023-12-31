from django.urls import path

from .views import dashboard, login_user, logout_user, task, task_detail_view, delivery, delivery_detail_view, \
    returns, returns_detail_view, order_item, order_item_detail_view, stock_item, stock_item_detail_view, admin_panel, \
    notification

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", login_user, name="login_user"),
    path('logout/', logout_user, name='logout_user'),
    path('task/', task, name='task'),
    path('task/<int:task_id>/', task_detail_view, name='task_detail_view'),
    path('delivery/', delivery, name='delivery'),
    path('delivery/<int:delivery_id>/', delivery_detail_view, name='delivery_detail_view'),
    path('return/', returns, name='returns'),
    path('return/<int:return_id>/', returns_detail_view, name='returns_detail_view'),
    path('order_item/', order_item, name='order_item'),
    path('order_item/<int:order_item_id>/', order_item_detail_view, name='order_item_detail_view'),
    path('stock_item/', stock_item, name='stock_item'),
    path('stock_item/<int:stock_item_id>/', stock_item_detail_view, name='stock_item_detail_view'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('notification/', notification, name='notification'),
]
