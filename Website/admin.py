from django.contrib import admin
from .models import UserProfile, Task, Delivery, Day, Return, OrderItem

admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Delivery)
admin.site.register(Day)
admin.site.register(Return)
admin.site.register(OrderItem)
