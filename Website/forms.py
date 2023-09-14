from django import forms
from .models import Task, Delivery, Return


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
