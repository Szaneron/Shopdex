
# Shopdex - E-commerce Workflow Management System

The project is a web application written in Python using the Django framework. The application is designed to organize the workflow for a growing e-commerce company. It allows for the management of deliveries, tasks, returns, items to be ordered, and the inventory.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Database structure](#database-structure)
- [Notifications](#notifications)
- [Requirements](#requirements)

## Features
- **Authentication**:
  - Different types of users can log in: regular users, administrators, and managers.
- **Dashboard**:
  - Displays the current working day, a calendar, and task, delivery, and return tables for the day.
  - A progress bar illustrating the day's progress based on completed tasks, deliveries, and returns.
- **Admin Panel**:
  - Five different forms for adding data: delivery, task, return, changing working hours for a specific day, and generating various PDFs based on specific data.
  - Presents a chart showing the number of tasks and deliveries over the last six months.
  - Displays all employee accounts along with their task performance rating calculations.
- **Tasks**:
  - Displays a table of tasks assigned for a specific day.
  - Interactive calendar to select the day for viewing data.
  - Detailed view for each task with actions like marking as completed, editing, and deletion.
- **Deliveries**:
  - Displays a table of deliveries scheduled for a specific day.
  - Detailed view for each delivery with actions like marking as received, marking as undelivered, editing, and deletion.
  - Allows adding comments to specific deliveries by all users.
- **Returns**:
  - Displays two tables: pending returns and received returns, offering clarity on the returns' status.
  - Detailed view for each return with actions like marking as prepared, marking as received, generating advice notes, editing, and deletion.
- **Order Items**:
  - Displays a table of items to be ordered.
  - Allows addition of new items.
  - Enables admins and managers to change item statuses (ordered or pending).
- **Warehouse**:
  - Displays a table of items currently in the warehouse.
  - Allows addition of new items and adjustment of item quantities.
- **Notifications**:
  - Provides a view for notifications, offering a central hub for updates on application activities.
- **PDF Generation**:
  - The application can generate PDF documents for various purposes, such as delivery     notes, order forms, and more.
  - PDFs can be generated directly from the admin panel, allowing easy access to essential documents for printing and record-keeping.


## Getting Started

### Prerequisites

- Django 4.2.4
- python-dotenv 1.0.0
- reportlab 4.0.4

### Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/Szaneron/Shopdex
  cd your-repository
  ```

2. Install dependencies::
  ```bash
  pip install -r requirements.txt
  ```

## Usage
Start the Django development server:
  ```bash
  python manage.py runserver
  ```
  Access the application via http://localhost:8000 in your web browser.

## Database structure
- **User Profile:**
  User profiles store additional information about users, including their profile pictures and statistics on assigned and completed tasks. The position field determines the user's role.
- **Comment:**
  Comments are related to various models in the system and store information about the user who added the comment, the related model's ID, and the comment's content.
- **Task:**
  Tasks represent work assignments within the system. They store information about the task name, description, status, assigned user, and comments related to the task.
- **Delivery:**
  Deliveries represent information about incoming shipments. They store details about the delivery company, delivery form, quantity of items, and related comments. The system generates additional context information, and invoice PDFs can be attached.
- **Day:**
  The Day model stores information about working hours, specifically the end-of-work hour for each day. Each day is uniquely identified by its date.
- **Return:**
  Returns store information about items to be returned. They include details about the return's name, description, status, and date. Additional information, such as the receiving company, notice, and notes, can also be added.
- **OrderItem:**
  OrderItems represent items that need to be ordered. They store information about the item's name, description, and status. The user who created the item can be associated with it.
- **StockItem:**
  StockItems represent items in the company's inventory. They include information about dimensions, usage, quantity, and the user who created the item.
- **Notification:**
  Notifications provide information about various activities within the system. They include details about the related model, the user who created the notification, and the users for whom the notification is relevant. Users can mark notifications as read.
  
![shopdex drawio](https://github.com/Szaneron/Shopdex/assets/58951668/86aea041-9781-4bc0-8328-9acbd72f77d9)

## Notifications
The application uses notifications to keep users informed about various events and activities. Notifications are sent for actions like adding a new delivery, marking a task as completed, or adding comments. These notifications help users stay updated and navigate directly to relevant views.

## Technologies Used
* Django 4.2.4
* python-dotenv 1.0.0
* reportlab 4.0.4
* jQuery 3.6.0
* SweetAlert
