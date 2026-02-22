#!/usr/bin/env python
"""
Test script for clearance workflow
Run with: python manage.py shell < clearance/test_workflow.py
"""

from django.contrib.auth import get_user_model
from students.models import StudentProfile
from departments.models import Department
from clearance.models import (
    ClearanceWorkflow, ClearanceSession, 
    ClearanceRecord, ClearanceComment
)
from django.utils import timezone

User = get_user_model()

def create_test_data():
    print("=" * 50)
    print("CREATING TEST DATA FOR CLEARANCE WORKFLOW")
    print("=" * 50)
    
    # 1. Create Users
    print("\n📝 Creating users...")
    
    # Admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@university.edu',
            'role': 'ADMIN'
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("  ✅ Admin created: admin/admin123")
    else:
        print("  ✅ Admin already exists")
    
    # Student user
    student_user, created = User.objects.get_or_create(
        username='teststudent',
        defaults={
            'email': 'student@university.edu',
            'role': 'STUDENT',
            'first_name': 'John',
            'last_name': 'Doe'
        }
    )
    if created:
        student_user.set_password('student123')
        student_user.save()
        print("  ✅ Student created: teststudent/student123")
    else:
        print("  ✅ Student already exists")
    
    # Officer users for different departments
    officers = []
    dept_officers = [
        ('library_officer', 'LIB123', 'library@univ.edu'),
        ('finance_officer', 'FIN123', 'finance@univ.edu'),
        ('hostel_officer', 'HOS123', 'hostel@univ.edu'),
        ('ict_officer', 'ICT123', 'ict@univ.edu'),
        ('faculty_officer', 'FAC123', 'faculty@univ.edu'),
    ]
    
    for username, password, email in dept_officers:
        officer, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': 'OFFICER',
                'first_name': f'Officer {username.split("_")[0].title()}'
            }
        )
        if created:
            officer.set_password(password)
            officer.save()
            print(f"  ✅ Officer created: {username}/{password}")
        else:
            print(f"  ✅ Officer {username} already exists")
        officers.append(officer)
    
    # 2. Create Student Profile
    print("\n📝 Creating student profile...")
    
    student_profile, created = StudentProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'admission_number': 'ADM2026001',
            'registration_number': 'REG2026001',
            'faculty': 'Engineering',
            'department': 'Computer Science',
            'course': 'Software Engineering',
            'year_of_study': 'Y4',
            'status': 'ACTIVE'
        }
    )
    if created:
        print(f"  ✅ Student profile created: {student_profile.admission_number}")
    else:
        print(f"  ✅ Student profile already exists")
    
    # 3. Create Departments if they don't exist
    print("\n📝 Setting up departments...")
    
    departments_data = [
        {'code': 'LIB001', 'name': 'University Library', 'type': 'LIBRARY', 'officer_idx': 0},
        {'code': 'FIN001', 'name': 'Finance Office', 'type': 'FINANCE', 'officer_idx': 1},
        {'code': 'HOS001', 'name': 'Student Hostels', 'type': 'HOSTEL', 'officer_idx': 2},
        {'code': 'ICT001', 'name': 'ICT Services', 'type': 'ICT', 'officer_idx': 3},
        {'code': 'FAC001', 'name': 'Faculty of Engineering', 'type': 'FACULTY', 'officer_idx': 4},
        {'code': 'REG001', 'name': 'Academic Registrar', 'type': 'FACULTY', 'officer_idx': 4},
    ]
    
    departments = []
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            code=dept_data['code'],
            defaults={
                'name': dept_data['name'],
                'department_type': dept_data['type'],
                'description': f'{dept_data["name"]} department',
                'is_active': True
            }
        )
        if created:
            print(f"  ✅ Department created: {dept.name}")
        else:
            print(f"  ✅ Department already exists: {dept.name}")
        
        # Assign officer
        dept.officers.add(officers[dept_data['officer_idx']])
        departments.append(dept)
    
    # 4. Get Graduation Workflow
    print("\n📝 Checking clearance workflow...")
    try:
        workflow = ClearanceWorkflow.objects.get(session_type='GRADUATION')
        print(f"  ✅ Workflow found: {workflow.name}")
        
        # Show stages - FIXED: Use correct related_name
        stages = workflow.stages.all().order_by('stage_order')
        print(f"\n📋 Workflow Stages:")
        for stage in stages:
            print(f"    Stage {stage.stage_order}: {stage.name}")
            # FIXED: Use 'departments' related_name instead of 'workflowstagedepartment_set'
            depts = stage.departments.all()
            for dept in depts:
                print(f"      - {dept.department.name} (Order: {dept.order_within_stage})")
    
    except ClearanceWorkflow.DoesNotExist:
        print("  ❌ Graduation workflow not found! Run migrations first.")
        return None
    
    print("\n" + "=" * 50)
    print("✅ TEST DATA CREATED SUCCESSFULLY")
    print("=" * 50)
    
    return {
        'student_user': student_user,
        'student_profile': student_profile,
        'officers': officers,
        'departments': departments,
        'workflow': workflow
    }

# Run the function
data = create_test_data()
