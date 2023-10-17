from django import forms
from .models import Task, Delivery, Return, OrderItem, StockItem, Day, Comment


class TaskEditForm(forms.ModelForm):
    # Form for editing a Task.
    # This form defines the fields and widgets for editing a Task using a ModelForm.

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_to', 'is_important', 'task_date']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'is_important': forms.CheckboxInput(),
            'task_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DeliveryEditForm(forms.ModelForm):
    # Form for editing a Delivery.
    # This form defines the fields and widgets for editing a Delivery using a ModelForm.

    class Meta:
        model = Delivery
        fields = ['delivery_company', 'form', 'quantity', 'description', 'status', 'delivery_date', 'invoice_pdf']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ReturnEditForm(forms.ModelForm):
    # Form for editing a Return.
    # This form defines the fields and widgets for editing a Return using a ModelForm.

    class Meta:
        model = Return
        fields = ['name', 'description', 'status', 'return_date', 'receiving_company', 'notice', 'wholesale', 'notes',
                  'package_quantity']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'notes': forms.Textarea(attrs={'rows': 5}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }


class OrderItemCreateForm(forms.ModelForm):
    # Form for creating an OrderItem.
    # This form defines the fields and widgets for creating an OrderItem using a ModelForm.

    class Meta:
        model = OrderItem
        fields = ['name', 'description']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class OrderItemEditForm(forms.ModelForm):
    # Form for editing an OrderItem.
    # This form defines the fields and widgets for editing an OrderItem using a ModelForm.

    class Meta:
        model = OrderItem
        fields = ['name', 'description', 'status']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class StockItemCreateForm(forms.ModelForm):
    # Form for creating a StockItem.
    # This form defines the fields and widgets for creating a StockItem using a ModelForm.

    class Meta:
        model = StockItem
        fields = ['dimensions', 'usage', 'quantity']

    widgets = {
        'usage': forms.Textarea(attrs={'rows': 5}),
    }


class StockItemEditForm(forms.ModelForm):
    # Form for editing a StockItem.
    # This form defines the fields and widgets for editing a StockItem using a ModelForm.

    class Meta:
        model = StockItem
        fields = ['dimensions', 'usage', 'quantity']

        widgets = {
            'usage': forms.Textarea(attrs={'rows': 5}),
        }


class AddDeliveryForm(forms.ModelForm):
    # Form for adding a new Delivery.
    # This form defines the fields and widgets for adding a new Delivery using a ModelForm.

    class Meta:
        model = Delivery
        fields = ['delivery_company', 'form', 'quantity', 'description', 'delivery_date', 'invoice_pdf']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

    invoice_pdf = forms.FileField(required=False)


class AddCommentForm(forms.ModelForm):
    # Form for adding a new Comment.
    # This form defines the fields and widgets for adding a new Comment using a ModelForm.
    class Meta:
        model = Comment
        fields = ['description']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class AddTaskForm(forms.ModelForm):
    # Form for adding a new Task.
    # This form defines the fields and widgets for adding a new Task using a ModelForm.

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'is_important', 'task_date']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'is_important': forms.CheckboxInput(),
            'task_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AddReturnForm(forms.ModelForm):
    # Form for adding a new Return.
    # This form defines the fields and widgets for adding a new Return using a ModelForm.

    class Meta:
        model = Return
        fields = ['name', 'description', 'return_date', 'receiving_company', 'notice', 'wholesale', 'notes',
                  'package_quantity']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'notes': forms.Textarea(attrs={'rows': 5}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DayForm(forms.ModelForm):
    # Form for creating and editing a Day.
    # This form defines the fields and widgets for creating and editing a Day model using a ModelForm.

    class Meta:
        model = Day
        fields = ['day_date', 'end_of_work_hour']

        widgets = {
            'day_date': forms.DateInput(attrs={'type': 'date'}),
            'end_of_work_hour': forms.TimeInput(attrs={'type': 'time'}), }
