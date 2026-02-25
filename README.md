# 🎓 University E-Clearance Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![DRF](https://img.shields.io/badge/DRF-3.14-red)
![JWT](https://img.shields.io/badge/JWT-Auth-orange)
![Celery](https://img.shields.io/badge/Celery-5.3-brightgreen)
![Redis](https://img.shields.io/badge/Redis-7.0-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Build](https://img.shields.io/badge/build-passing-success)
![Version](https://img.shields.io/badge/version-2.0.0-blue)

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/Opwondo/University_E_Clearance)
[![Documentation](https://img.shields.io/badge/docs-API-blue)](http://localhost:8000/api/)
[![Demo](https://img.shields.io/badge/demo-available-brightgreen)](http://localhost:8000/api/reports/dashboard/)

</div>

A comprehensive **Django REST API** for automating university student clearance processes. This system digitizes the traditional manual clearance workflow, allowing students to request clearance and departments to approve/reject requests seamlessly with real-time notifications, audit trails, and certificate generation.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [User Roles & Permissions](#-user-roles--permissions)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

The University E-Clearance Management System replaces paper-based, manual clearance processes with a centralized digital platform. Students can track their clearance status in real-time, while department officers can efficiently manage approval workflows.

### Problem Statement
Traditional university clearance involves students physically visiting multiple departments (Library, Finance, Hostel, ICT, Faculty, etc.) to obtain signatures - a time-consuming, inefficient process prone to errors, lost documents, and long queues.

### Solution
This system provides:
- **Centralized Platform**: All clearance requests managed in one place
- **Real-time Tracking**: Students can monitor their clearance progress
- **Automated Workflows**: Streamlined approval processes with hybrid stage logic
- **Role-based Access**: Secure access for Students, Officers, and Administrators
- **Digital Records**: Permanent, searchable audit trail of all actions
- **Instant Notifications**: Email alerts for status changes and pending tasks
- **Certificate Generation**: Automated PDF certificates upon completion

---

## ✨ Features

### 🔐 **Authentication & Authorization**
| Feature | Status |
|---------|--------|
| ✅ JWT-based authentication | Complete |
| ✅ Role-based access control (Student, Officer, Admin) | Complete |
| ✅ Custom permission classes | Complete |
| ✅ Token refresh mechanism | Complete |
| ✅ Password hashing and security | Complete |

### 👥 **User Management**
| Feature | Status |
|---------|--------|
| ✅ Custom User model with roles | Complete |
| ✅ Student profile management | Complete |
| ✅ Department officer assignment | Complete |
| ✅ Account activation/deactivation | Complete |

### 🏛️ **Department Management**
| Feature | Status |
|---------|--------|
| ✅ Department categorization (Library, Finance, Hostel, ICT, etc.) | Complete |
| ✅ Officer assignment to departments | Complete |
| ✅ Hierarchical department structure | Complete |
| ✅ Department performance tracking | Complete |

### 🔄 **Clearance Workflow**
| Feature | Status |
|---------|--------|
| ✅ Hybrid workflow with sequential stages | Complete |
| ✅ Parallel approvals within stages | Complete |
| ✅ Automatic stage progression | Complete |
| ✅ Blocked status on rejections | Complete |
| ✅ Real-time progress tracking (%) | Complete |
| ✅ Current stage detection | Complete |
| ✅ Clearance session management | Complete |
| ✅ Department approval/rejection with remarks | Complete |

### 📧 **Email Notifications**
| Feature | Status |
|---------|--------|
| ✅ Async email sending with Celery | Complete |
| ✅ Redis message broker | Complete |
| ✅ Session created notification | Complete |
| ✅ Department approved notification | Complete |
| ✅ Department rejected notification | Complete |
| ✅ Session completed notification | Complete |
| ✅ Daily pending reminders for officers | Complete |
| ✅ Email tracking with status monitoring | Complete |

### 🔍 **Audit Logging**
| Feature | Status |
|---------|--------|
| ✅ Comprehensive audit trail | Complete |
| ✅ Before/after state tracking with JSON | Complete |
| ✅ IP address and user agent capture | Complete |
| ✅ Color-coded admin interface | Complete |
| ✅ Filtering by action type, user, date | Complete |
| ✅ Entity-specific log tracking | Complete |
| ✅ Statistics dashboard | Complete |

### 📊 **Reporting & Analytics**
| Feature | Status |
|---------|--------|
| ✅ Interactive HTML dashboard | Complete |
| ✅ Clearance trends visualization | Complete |
| ✅ Department performance metrics | Complete |
| ✅ Student progress tracking | Complete |
| ✅ Activity heatmap | Complete |
| ✅ Completion rates analytics | Complete |
| ✅ Response time metrics | Complete |
| ✅ Data export (JSON/CSV ready) | Complete |
| ✅ Chart.js integration | Complete |

### 📄 **PDF Certificate Generation**
| Feature | Status |
|---------|--------|
| ✅ Automated certificate generation | Complete |
| ✅ Unique certificate numbers | Complete |
| ✅ Verification codes (UUID-based) | Complete |
| ✅ Public certificate verification | Complete |
| ✅ Download tracking | Complete |
| ✅ Professional HTML/CSS templates | Complete |
| ✅ University branding | Complete |
| ✅ A4 landscape formatting | Complete |

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core programming language |
| Django | 4.2 | Web framework |
| Django REST Framework | 3.14 | API development |
| SQLite | 3.x | Development database |
| PostgreSQL | 14.x | Production database |

### Authentication & Security
| Technology | Purpose |
|------------|---------|
| JWT (SimpleJWT) | Token-based authentication |
| Bcrypt | Password hashing |
| CORS headers | Cross-origin resource sharing |

### Task Queue & Email
| Technology | Purpose |
|------------|---------|
| Celery | Async task processing |
| Redis | Message broker |
| SMTP | Email sending |
| django-anymail | Email backend abstraction |

### PDF Generation
| Technology | Purpose |
|------------|---------|
| WeasyPrint | PDF generation from HTML/CSS |
| django-weasyprint | Django integration |

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 | Structure |
| CSS3 | Styling |
| JavaScript | Interactivity |
| Chart.js | Data visualization |

### Development Tools
| Tool | Purpose |
|------|---------|
| Git & GitHub | Version control |
| Postman | API testing |
| VS Code | IDE |
| Black | Code formatting |
| Flake8 | Linting |

---
## 📁 Project Structure
```

University_E_Clearance/
├── 📁 accounts/ # User management app
│ ├── 📄 models.py # Custom User model with roles
│ ├── 📄 permissions.py # Role-based permissions
│ ├── 📄 serializers.py # User serializers
│ ├── 📄 views.py # Authentication views
│ └── 📄 urls.py # Auth endpoints
│
├── 📁 students/ # Student management app
│ ├── 📄 models.py # StudentProfile model
│ ├── 📄 serializers.py # Student serializers
│ ├── 📄 views.py # Student CRUD views
│ └── 📄 urls.py # Student endpoints
│
├── 📁 departments/ # Department management app
│ ├── 📄 models.py # Department model
│ ├── 📄 serializers.py # Department serializers
│ ├── 📄 views.py # Department CRUD views
│ └── 📄 urls.py # Department endpoints
│
├── 📁 clearance/ # Core clearance workflow app
│ ├── 📄 models.py # WorkflowStage, ClearanceSession, etc.
│ ├── 📄 serializers.py # Clearance serializers
│ ├── 📄 views.py # Clearance workflow views
│ ├── 📄 views_email.py # Email notification views
│ ├── 📄 utils/ # Utility functions
│ │ ├── 📄 init.py
│ │ └── 📄 email_utils.py # Email sending logic
│ ├── 📄 templates/emails/ # Email templates
│ │ ├── 📄 session_created.html
│ │ ├── 📄 record_approved.html
│ │ ├── 📄 record_rejected.html
│ │ ├── 📄 session_completed.html
│ │ └── 📄 pending_reminder.html
│ └── 📄 urls.py # Clearance endpoints
│
├── 📁 audit/ # Audit logging app
│ ├── 📄 models.py # AuditLog model
│ ├── 📄 middleware.py # Request logging middleware
│ ├── 📄 serializers.py # Audit serializers
│ ├── 📄 views.py # Audit API endpoints
│ └── 📄 urls.py # Audit routes
│
├── 📁 reports/ # Reporting & analytics app
│ ├── 📄 models.py # Statistics models
│ ├── 📄 serializers.py # Report serializers
│ ├── 📄 views.py # Analytics endpoints
│ ├── 📄 templates/reports/ # Dashboard templates
│ │ └── 📄 dashboard.html # Interactive dashboard
│ └── 📄 urls.py # Report endpoints
│
├── 📁 certificates/ # PDF certificate app
│ ├── 📄 models.py # Certificate models
│ ├── 📄 serializers.py # Certificate serializers
│ ├── 📄 views.py # Certificate generation views
│ ├── 📄 templates/certificates/ # Certificate templates
│ │ ├── 📄 base_certificate.html
│ │ └── 📄 graduation_certificate.html
│ └── 📄 urls.py # Certificate endpoints
│
├── 📁 e_clearance/ # Project configuration
│ ├── 📄 settings.py # Django settings
│ ├── 📄 urls.py # Main URL configuration
│ ├── 📄 celery.py # Celery configuration
│ └── 📄 wsgi.py
│
├── 📁 media/ # User uploaded files
│ └── 📁 certificates/ # Generated PDF certificates
│
├── 📄 manage.py
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 .gitignore
└── 📄 README.md
```
---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)
- Git
- Redis (for Celery tasks)
- PostgreSQL (optional, for production)

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Opwondo/University_E_Clearance.git
cd University_E_Clearance
```
2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
nano .env
```
5. Apply Database Migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations students
python manage.py makemigrations departments
python manage.py makemigrations clearance
python manage.py makemigrations audit
python manage.py makemigrations reports
python manage.py makemigrations certificates
python manage.py migrate
```
6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts:

Username: admin

Email: admin@example.com

Password: ChooseAStrongPassword123!

7. Start Redis (for Celery)
```bash
# In a separate terminal
redis-server
```
8. Start Celery Worker
```bash
# In a separate terminal
cd University_E_Clearance
source venv/bin/activate
celery -A e_clearance worker --loglevel=info
```
9. Run Development Server
```bash
python manage.py runserver
```
