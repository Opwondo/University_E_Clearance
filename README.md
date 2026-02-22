# University E-Clearance Management System

A comprehensive Django REST API for automating university student clearance processes. This system digitizes the traditional manual clearance workflow, allowing students to request clearance and departments to approve/reject requests seamlessly.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)

## 🎯 Overview

The University E-Clearance Management System replaces paper-based, manual clearance processes with a centralized digital platform. Students can track their clearance status in real-time, while department officers can efficiently manage approval workflows.

### Problem Statement
Traditional university clearance involves students physically visiting multiple departments (Library, Finance, Hostel, ICT, etc.) to obtain signatures - a time-consuming, inefficient process prone to errors and document loss.

### Solution
This system provides:
- Centralized digital clearance requests
- Real-time status tracking
- Role-based access control (Students, Officers, Admin)
- Automated clearance status calculation
- Audit logs for all actions
- Email notifications for status changes

## ✨ Features

### Implemented ✅
- **JWT Authentication** - Secure token-based authentication
- **Role-Based Access Control** - Student, Officer, Admin roles
- **Student Profile Management** - Complete student records
- **Department Management** - Clearance units configuration

### In Progress 🚧
- **Clearance Workflow** - Request and approval system
- **Audit Logging** - Track all system actions
- **Reporting & Analytics** - Clearance statistics
- **Email Notifications** - Status change alerts
- **PDF Generation** - Clearance certificates

## 🛠 Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: JWT (django-rest-framework-simplejwt)
- **Documentation**: Coming soon
- **Testing**: Django Test Framework
- **Version Control**: Git

## 📁 Project Structure

```bash
University_E_Clearance/
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── permissions.py
│   ├── __pycache__
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── audit
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── clearance
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── departments
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── e_clearance
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── README.md
├── requirements.txt
├── students
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    └── pyvenv.cfg
...
```




## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/University_E_Clearance.git
cd University_E_Clearance

