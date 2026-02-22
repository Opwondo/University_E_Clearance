#!/usr/bin/env python
"""
Comprehensive test script for clearance workflow
Run with: python manage.py shell < clearance/test_full_workflow.py
"""

import json
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from students.models import StudentProfile
from departments.models import Department
from clearance.models import ClearanceWorkflow, ClearanceSession, ClearanceRecord

User = get_user_model()

class ClearanceWorkflowTester:
    def __init__(self):
        self.client = APIClient()
        self.setup_test_data()
    
    def setup_test_data(self):
        """Create or get test users and data"""
        print("\n🔧 Setting up test data...")
        
        # Get or create admin
        self.admin = User.objects.filter(role='ADMIN').first()
        if not self.admin:
            self.admin = User.objects.create_user(
                username='admin_tester',
                password='admin123',
                email='admin@test.edu',
                role='ADMIN'
            )
            print("  ✅ Created admin user")
        
        # Get or create student
        self.student_user = User.objects.filter(role='STUDENT').first()
        if not self.student_user:
            self.student_user = User.objects.create_user(
                username='student_tester',
                password='student123',
                email='student@test.edu',
                role='STUDENT'
            )
            print("  ✅ Created student user")
            
            # Create student profile
            self.student = StudentProfile.objects.create(
                user=self.student_user,
                admission_number='TEST001',
                registration_number='TESTREG001',
                faculty='Engineering',
                department='Computer Science',
                course='Software Engineering',
                year_of_study='Y4'
            )
            print("  ✅ Created student profile")
        else:
            self.student = StudentProfile.objects.get(user=self.student_user)
            print("  ✅ Using existing student")
        
        # Get officers and departments
        self.officers = User.objects.filter(role='OFFICER')
        self.departments = Department.objects.all()
        
        # Get workflow
        try:
            self.workflow = ClearanceWorkflow.objects.get(session_type='GRADUATION')
            print("  ✅ Workflow found")
        except ClearanceWorkflow.DoesNotExist:
            print("  ❌ Workflow not found! Run migrations first.")
            self.workflow = None
        
        print("  ✅ Test data ready")
    
    def test_full_flow(self):
        """Test complete clearance workflow"""
        if not self.workflow:
            print("\n❌ Cannot run tests without workflow")
            return
        
        print("\n" + "=" * 60)
        print("🧪 TESTING COMPLETE CLEARANCE WORKFLOW")
        print("=" * 60)
        
        # Test 1: Student authentication
        print("\n1️⃣ Testing student authentication...")
        response = self.client.post('/api/auth/login/', {
            'username': self.student_user.username,
            'password': 'student123'
        })
        if response.status_code == 200:
            self.student_token = response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
            print("  ✅ Student login successful")
        else:
            print(f"  ❌ Login failed: {response.status_code}")
            print(f"  Response: {response.data}")
            return
        
        # Test 2: Get student summary
        print("\n2️⃣ Getting student summary...")
        response = self.client.get('/api/clearance/student/summary/')
        if response.status_code == 200:
            print(f"  ✅ Student summary: {response.data}")
        else:
            print(f"  ❌ Failed: {response.status_code}")
            print(f"  Response: {response.data}")
        
        # Test 3: Create clearance session
        print("\n3️⃣ Creating clearance session...")
        response = self.client.post('/api/clearance/sessions/', {
            'workflow': self.workflow.id
        })
        if response.status_code == 201:
            self.session_id = response.data['id']
            print(f"  ✅ Session created: {self.session_id}")
            print(f"  📊 Progress: {response.data.get('progress_percentage', 0)}%")
        else:
            print(f"  ❌ Failed: {response.status_code}")
            print(f"  Error: {response.data}")
            return
        
        # Test 4: Get session details
        print("\n4️⃣ Getting session details...")
        response = self.client.get(f'/api/clearance/sessions/{self.session_id}/')
        if response.status_code == 200:
            print(f"  ✅ Session status: {response.data['status']}")
            print(f"  📊 Records: {len(response.data.get('records', []))}")
            # Print record statuses
            for record in response.data.get('records', []):
                dept_name = record.get('department_details', {}).get('name', 'Unknown')
                status = record.get('status', 'Unknown')
                print(f"    - {dept_name}: {status}")
        else:
            print(f"  ❌ Failed: {response.status_code}")
        
        # Test 5: Login as library officer
        print("\n5️⃣ Testing officer authentication...")
        library_officer = User.objects.filter(username='library_officer').first()
        if library_officer:
            response = self.client.post('/api/auth/login/', {
                'username': 'library_officer',
                'password': 'LIB123'
            })
            if response.status_code == 200:
                self.officer_token = response.data['access']
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.officer_token}')
                print("  ✅ Library officer login successful")
            else:
                print(f"  ❌ Officer login failed: {response.status_code}")
                print(f"  Response: {response.data}")
                return
        else:
            print("  ⚠️ Library officer not found, skipping officer tests")
            return
        
        # Test 6: Get pending clearances for officer
        print("\n6️⃣ Getting pending clearances...")
        response = self.client.get('/api/clearance/pending/')
        if response.status_code == 200:
            print(f"  ✅ Found {len(response.data)} pending clearances")
            if response.data:
                self.record_id = response.data[0]['id']
                dept_name = response.data[0].get('department_details', {}).get('name', 'Unknown')
                print(f"  📝 First record: {dept_name} (ID: {self.record_id})")
        else:
            print(f"  ❌ Failed: {response.status_code}")
            print(f"  Response: {response.data}")
            return
        
        # Test 7: Approve a clearance
        if hasattr(self, 'record_id'):
            print("\n7️⃣ Approving clearance record...")
            response = self.client.post(f'/api/clearance/records/{self.record_id}/approve/', {
                'remarks': 'All requirements satisfied. Approved.'
            })
            if response.status_code == 200:
                print(f"  ✅ Record approved: {response.data['status']}")
            else:
                print(f"  ❌ Approval failed: {response.status_code}")
                print(f"  Error: {response.data}")
        
        # Test 8: Check session progress again
        print("\n8️⃣ Checking updated session progress...")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.get(f'/api/clearance/sessions/{self.session_id}/')
        if response.status_code == 200:
            print(f"  ✅ Updated progress: {response.data.get('progress_percentage', 0)}%")
            print(f"  📊 Records status:")
            for record in response.data.get('records', []):
                dept_name = record.get('department_details', {}).get('name', 'Unknown')
                status = record.get('status', 'Unknown')
                print(f"    - {dept_name}: {status}")
        else:
            print(f"  ❌ Failed: {response.status_code}")
        
        print("\n" + "=" * 60)
        print("✅ WORKFLOW TEST COMPLETED")
        print("=" * 60)

# Run the tests
if __name__ == '__main__':
    tester = ClearanceWorkflowTester()
    tester.test_full_flow()
