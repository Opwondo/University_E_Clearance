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
