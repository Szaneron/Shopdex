from django import forms
from .models import Task, Delivery, Return, OrderItem, StockItem


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_to', 'is_important', 'task_date']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
            'is_important': forms.CheckboxInput(),
            'task_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DeliveryEditForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_company', 'form', 'quantity', 'description', 'status', 'delivery_date']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ReturnEditForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['name', 'description', 'status', 'return_date', 'receiving_company', 'notice', 'wholesale', 'notes',
                  'package_quantity']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
            'notes': forms.Textarea(attrs={'rows': 10}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }


class OrderItemCreateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['name', 'description']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
        }


class OrderItemEditForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['name', 'description', 'status']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
        }


class StockItemCreateForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ['dimensions', 'usage', 'quantity']

    widgets = {
        'usage': forms.Textarea(attrs={'rows': 10}),
    }
