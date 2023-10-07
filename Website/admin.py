from django.contrib import admin
from .models import UserProfile, Task, Delivery, Day, Return, OrderItem, StockItem, Notification, Comment


class TaskAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'description',
        'status',
        'assigned_to',
        'is_important',
        'task_date',
        'creation_time',
    )
    list_display = ('task_combine_name_and_date', 'status', 'assigned_to', 'is_important')
    list_display_links = ('task_combine_name_and_date',)
    list_filter = ('status', 'assigned_to', 'is_important')
    search_fields = ('name', 'description', 'task_date')

    @staticmethod
    def task_combine_name_and_date(self):
        return "{} - {}".format(self.name, self.task_date.strftime("%d %m %Y"))


class DeliveryAdmin(admin.ModelAdmin):
    fields = (
        'delivery_company',
        'form',
        'quantity',
        'description',
        'status',
        'delivery_date',
        'creation_time',
        'comments',
        'generated_context',
    )
    list_display = ('delivery_combine_company_and_date', 'form', 'quantity', 'status')
    list_display_links = ('delivery_combine_company_and_date',)
    list_filter = ('delivery_company', 'status')
    search_fields = ('delivery_company', 'description', 'delivery_date')

    @staticmethod
    def delivery_combine_company_and_date(self):
        return "{} - {}".format(self.delivery_company, self.delivery_date.strftime("%d %m %Y"))


class DayAdmin(admin.ModelAdmin):
    fields = (
        'end_of_work_hour',
        'day_date',
    )
    list_display = ('day_date_field', 'end_time_field',)
    list_display_links = ('day_date_field',)
    search_fields = ('day_date',)

    @staticmethod
    def day_date_field(self):
        return '{}'.format(self.day_date.strftime("%d %m %Y"))

    @staticmethod
    def end_time_field(self):
        return '{}'.format(self.end_of_work_hour.strftime('%H:%M'))


class ReturnAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'description',
        'status',
        'return_date',
        'creation_time',
        'receiving_company',
        'notice',
        'wholesale',
        'notes',
        'package_quantity',
    )
    list_display = ('return_combine_name_and_date', 'status', 'receiving_company', 'notice')
    list_display_links = ('return_combine_name_and_date',)
    list_filter = ('status', 'receiving_company')
    search_fields = ('name', 'description', 'return_date',)

    @staticmethod
    def return_combine_name_and_date(self):
        return "{} - {}".format(self.name, self.return_date.strftime("%d %m %Y"))


class OrderItemAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'description',
        'status',
        'creation_time',
        'created_by',
    )
    list_display = ('name', 'status', 'created_by', 'creation_date_field')
    list_display_links = ('name',)
    list_filter = ('status',)
    search_fields = ('name', 'description')

    @staticmethod
    def creation_date_field(self):
        return '{}'.format(self.creation_time.strftime("%d %m %Y - %H:%M"))


class StockItemAdmin(admin.ModelAdmin):
    fields = (
        'dimensions',
        'usage',
        'quantity',
        'created_by'
    )
    list_display = ('dimensions', 'quantity', 'created_by')
    list_display_links = ('dimensions',)
    list_filter = ('created_by',)
    search_fields = ('dimensions', 'usage')


class NotificationAdmin(admin.ModelAdmin):
    fields = (
        'model_name',
        'model_id',
        'description',
        'read_by',
        'creation_time',
        'notify_for',
        'made_by',
    )
    list_display = ('notification_combine_name_and_date', 'model_id', 'notify_for', 'made_by', 'creation_date_field')
    list_display_links = ('notification_combine_name_and_date',)
    list_filter = ('notify_for', 'made_by')
    search_fields = ('model_name', 'description')

    @staticmethod
    def notification_combine_name_and_date(self):
        return '{} - {}'.format(self.model_name, self.creation_time.strftime("%d %m %Y"))

    @staticmethod
    def creation_date_field(self):
        return '{}'.format(self.creation_time.strftime("%d %m %Y - %H:%M"))


admin.site.register(UserProfile)
admin.site.register(Task, TaskAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Return, ReturnAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(StockItem, StockItemAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Comment)
