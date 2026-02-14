# University E-Clearance Management System

A comprehensive Django REST API for automating university student clearance processes. This system digitizes the traditional manual clearance workflow, allowing students to request clearance and departments to approve/reject requests seamlessly.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

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
- **Documentation**: OpenAPI (drf-yasg) - Coming soon
- **Testing**: Django Test Framework
- **Version Control**: Git

## 📁 Project Structure


University_E_Clearance/
├── e_clearance/ # Project configuration
│ ├── settings.py # Django settings
│ ├── urls.py # Main URL configuration
│ └── wsgi.py
├── accounts/ # User management app
│ ├── models.py # Custom User model
│ ├── serializers.py # User serializers
│ ├── views.py # Authentication views
│ ├── permissions.py # Role-based permissions
│ └── urls.py # Auth endpoints
├── students/ # Student management app
│ ├── models.py # StudentProfile model
│ ├── serializers.py # Student serializers
│ ├── views.py # Student CRUD views
│ └── urls.py # Student endpoints
├── departments/ # Department management app
│ ├── models.py # Department model
│ ├── serializers.py # Department serializers
│ ├── views.py # Department CRUD views
│ └── urls.py # Department endpoints
├── clearance/ # Clearance workflow app
│ ├── models.py # ClearanceRecord model
│ ├── serializers.py # Clearance serializers
│ ├── views.py # Clearance workflow views
│ └── urls.py # Clearance endpoints
├── audit/ # Audit logging app
│ ├── models.py # AuditLog model
│ ├── middleware.py # Request logging middleware
│ └── urls.py # Audit endpoints
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md


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

