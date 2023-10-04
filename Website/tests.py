from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.utils import timezone
from unittest.mock import Mock, MagicMock
from Website.models import Task, UserProfile, Delivery, Return
from Website.models import Notification
from Website.views import add_notification, get_employee_rating, generate_return_pdf, get_progress_bar_data


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.task = Task.objects.create(name="Task 1", task_date=timezone.now(), assigned_to=self.user_profile)

    def test_str_representation(self):
        # Test if the string representation of the task is as expected
        self.assertEqual(str(self.task), "Task 1 - " + str(self.task.task_date))

    def test_default_status(self):
        # Test if the default status of the task is 'Do zrobienia' (To do)
        self.assertEqual(self.task.status, 'Do zrobienia')

    def test_update_task(self):
        # Test updating the task name and confirming the update
        self.task.name = "Updated Task"
        self.task.save()
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.name, "Updated Task")

    def test_delete_task(self):
        # Test deleting a task and confirming it no longer exists
        task_pk = self.task.pk
        self.task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=task_pk)


class DeliveryModelTest(TestCase):
    def setUp(self):
        self.delivery = Delivery.objects.create(
            delivery_company='DPD',
            quantity=10,
            description='Test delivery description',
            status='W drodze',
            delivery_date=timezone.now(),
            creation_time=timezone.now(),
            generated_context='Test context'
        )

    def test_str_representation(self):
        # Test if the string representation of the delivery is as expected
        expected_str = f"{self.delivery.delivery_company} - {self.delivery.delivery_date}"
        self.assertEqual(str(self.delivery), expected_str)

    def test_default_form(self):
        # Test if the default form of the delivery is 'Paczka'
        self.assertEqual(self.delivery.form, 'Paczka')

    def test_valid_status(self):
        # Test if the status of the delivery is one of the valid choices
        # The status should be one of the keys from the STATUS_CHOICES dictionary in the Delivery model
        self.assertIn(self.delivery.status, dict(Delivery.STATUS_CHOICES).keys())


class ReturnModelTest(TestCase):
    def setUp(self):
        self.return_item = Return.objects.create(
            name='Test Return',
            description='Test return description',
            return_date=timezone.now(),
            creation_time=timezone.now(),
            receiving_company='Test Company',
            notice='Test Notice',
            wholesale='Test Wholesale',
            notes='Test notes',
        )

    def test_str_representation(self):
        # Test if the string representation of the return is as expected
        expected_str = f"{self.return_item.name} - {self.return_item.return_date}"
        self.assertEqual(str(self.return_item), expected_str)

    def test_default_status(self):
        # Test if the default status of the return is 'Do spakowania' (To be packed)
        self.assertEqual(self.return_item.status, 'Do spakowania')

    def test_valid_status(self):
        # Test if the status of the return is one of the valid choices
        # The status should be one of the keys from the STATUS_CHOICES dictionary in the Return model
        self.assertIn(self.return_item.status, dict(Return.STATUS_CHOICES).keys())

    def test_package_quantity_non_negative(self):
        # Test if default packaging quantity returned is non-negative
        self.assertGreaterEqual(self.return_item.package_quantity, 1)


class ProgressBarDataCalculationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.task = Task.objects.create(name="Task 1", task_date=timezone.now(), assigned_to=self.user_profile)
        self.task = Task.objects.create(name="Task 2", task_date=timezone.now(), assigned_to=self.user_profile)

        self.delivery = Delivery.objects.create(
            delivery_company='DPD',
            quantity=10,
            description='Test delivery description',
            status='W drodze',
            delivery_date=timezone.now(),
            creation_time=timezone.now(),
            generated_context='Test context'
        )

        self.return_item = Return.objects.create(
            name='Test Return',
            description='Test return description',
            return_date=timezone.now(),
            creation_time=timezone.now(),
            receiving_company='Test Company',
            notice='Test Notice',
            wholesale='Test Wholesale',
            notes='Test notes',
        )
        self.all_tasks = Task.objects.all()
        self.all_delivery = Delivery.objects.all()
        self.all_return = Return.objects.all()

    def test_get_progress_bar_data(self):
        # Call the function to calculate progress bar data
        progress_bar_data = get_progress_bar_data(self.all_tasks, self.all_delivery, self.all_return)

        # Expected calculations
        expected_all_to_do = self.all_tasks.count() + self.all_delivery.count() + self.all_return.count()  # Total number of tasks, deliveries, and returns
        expected_all_done = 0  # Assuming no tasks, deliveries, or returns are marked as 'done'
        expected_percentage_done = 0  # No tasks, deliveries, or returns are 'done'

        # Assert the progress bar data matches the expected values
        self.assertEqual(progress_bar_data['all_to_do'], expected_all_to_do)
        self.assertEqual(progress_bar_data['all_done'], expected_all_done)
        self.assertEqual(progress_bar_data['percentage_done'], expected_percentage_done)

    def test_get_progress_bar_data_with_completed_tasks(self):
        # Call the function to calculate progress bar data
        task_to_update = Task.objects.get(name='Task 1')
        task_to_update.status = 'Zrobione'
        task_to_update.save()
        progress_bar_data = get_progress_bar_data(self.all_tasks, self.all_delivery, self.all_return)

        # Expected calculations
        expected_all_to_do = self.all_tasks.count() + self.all_delivery.count() + self.all_return.count()  # Total number of tasks, deliveries, and returns
        expected_all_done = 1  # One tasks are marked as 'done'
        expected_percentage_done = 25  # Percentage of completion

        # Assert the progress bar data matches the expected values
        self.assertEqual(progress_bar_data['all_to_do'], expected_all_to_do)
        self.assertEqual(progress_bar_data['all_done'], expected_all_done)
        self.assertEqual(progress_bar_data['percentage_done'], expected_percentage_done)


class EmployeeRatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_no_tasks(self):
        # Test if we receive the appropriate message for missing tasks
        rating = get_employee_rating(self.user)
        self.assertEqual(rating, 'Brak zadań')

    def test_valid_rating(self):
        # Test if the rating is calculated correctly for tasks
        self.user_profile.assigned_tasks = 10
        self.user_profile.completed_tasks = 5
        self.user_profile.save()

        rating = get_employee_rating(self.user)
        self.assertEqual(rating, 2.5)

    def test_min_rating(self):
        # Test if the minimum rating is 1 for no tasks completed
        self.user_profile.assigned_tasks = 5
        self.user_profile.completed_tasks = 0
        self.user_profile.save()

        rating = get_employee_rating(self.user)
        self.assertEqual(rating, 1)

    def test_max_rating(self):
        # Test if the maximum rating is 5 for all completed tasks
        self.user_profile.assigned_tasks = 5
        self.user_profile.completed_tasks = 5
        self.user_profile.save()

        rating = get_employee_rating(self.user)
        self.assertEqual(rating, 5)


class ReturnPDFGenerationTest(TestCase):

    def setUp(self):
        # Set up any necessary data for the tests
        self.return_item = Return.objects.create(
            name='Test Return',
            description='Test return description',
            return_date=timezone.now(),
            creation_time=timezone.now(),
            receiving_company='Test Company',
            notice='Test Notice',
            wholesale='Test Wholesale',
            notes='Test notes',
        )
        self.return_id = self.return_item.id

    def test_generate_return_pdf(self):
        # Call the function to generate the PDF
        response = generate_return_pdf(self.return_id)
        return_data = get_object_or_404(Return, id=self.return_id)

        # Assert the response content type is application/pdf
        self.assertEqual(response['Content-Type'], 'application/pdf')

        # Assert the content disposition header includes the return ID in the filename
        expected_filename = f'return_{return_data.name}_{return_data.return_date}.pdf'
        self.assertIn(expected_filename, response['Content-Disposition'])

        # Assert that the response has a non-empty content
        self.assertTrue(response.content)


class NotificationUtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user_profile = UserProfile.objects.create(user=self.user, position='Pracownik')

    def test_add_notification_employee(self):
        # Test if the notification is added correctly for the user with the 'Employee' position
        target_model = Task.objects.create(name="Test Model", task_date=timezone.now(),
                                           assigned_to=self.user_profile)
        add_notification(self.user, target_model, 'Test Notification', 'Test description')
        notification = Notification.objects.get(model_id=target_model.id)
        self.assertEqual(notification.notify_for, 'Other')

    def test_add_notification_other(self):
        # Test if the notification is correctly added for a user with a position other than 'Employee'
        self.user_profile.position = 'Admin'
        self.user_profile.save()
        target_model = Task.objects.create(name='Test Model', assigned_to=self.user_profile)
        add_notification(self.user, target_model, 'Test Notification', 'Test description')
        notification = Notification.objects.get(model_id=target_model.id)
        self.assertEqual(notification.notify_for, 'Pracownik')

    def test_add_notification_description(self):
        # Test if the notification description is assigned correctly
        target_model = Task.objects.create(name='Test Model', assigned_to=self.user_profile)
        add_notification(self.user, target_model, 'Test Notification Model Name', 'Test description')
        notification = Notification.objects.get(model_id=target_model.id)
        self.assertEqual(notification.description, 'Test description')
