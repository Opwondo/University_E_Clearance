from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Department

User = get_user_model()

class DepartmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='ADMIN'
        )
        
        self.department = Department.objects.create(
            name='University Library',
            code='LIB001',
            department_type='LIBRARY',
            description='Main university library'
        )
    
    def test_department_creation(self):
        self.assertEqual(self.department.name, 'University Library')
        self.assertEqual(self.department.code, 'LIB001')
        self.assertEqual(self.department.department_type, 'LIBRARY')
        self.assertTrue(self.department.is_active)
    
    def test_department_str_method(self):
        expected = 'University Library (LIB001)'
        self.assertEqual(str(self.department), expected)
    
    def test_pending_clearances_count(self):
        # Initially should be 0
        self.assertEqual(self.department.get_pending_clearances(), 0)

class DepartmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create users with different roles
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            role='ADMIN'
        )
        
        self.officer = User.objects.create_user(
            username='officer',
            password='officer123',
            role='OFFICER'
        )
        
        self.student = User.objects.create_user(
            username='student',
            password='student123',
            role='STUDENT'
        )
        
        # Create test department
        self.department = Department.objects.create(
            name='ICT Department',
            code='ICT001',
            department_type='ICT',
            description='Information Technology'
        )
        self.department.officers.add(self.officer)
    
    def test_list_departments_authenticated(self):
        """Authenticated users should be able to list departments"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_departments_unauthenticated(self):
        """Unauthenticated users should not access departments"""
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_department_admin(self):
        """Admin should be able to create department"""
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': 'Finance Department',
            'code': 'FIN001',
            'department_type': 'FINANCE',
            'description': 'Finance office'
        }
        response = self.client.post('/api/departments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)
    
    def test_create_department_officer(self):
        """Officer should not be able to create department"""
        self.client.force_authenticate(user=self.officer)
        data = {
            'name': 'Finance Department',
            'code': 'FIN001',
            'department_type': 'FINANCE',
            'description': 'Finance office'
        }
        response = self.client.post('/api/departments/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_department_officer(self):
        """Officer should be able to update their department"""
        self.client.force_authenticate(user=self.officer)
        data = {'description': 'Updated description'}
        response = self.client.patch(f'/api/departments/{self.department.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.description, 'Updated description')
    
    def test_update_department_student(self):
        """Student should not be able to update department"""
        self.client.force_authenticate(user=self.student)
        data = {'description': 'Updated description'}
        response = self.client.patch(f'/api/departments/{self.department.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_department_admin(self):
        """Admin should be able to delete department"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/departments/{self.department.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)
    
    def test_add_officers_to_department(self):
        """Admin should be able to add officers to department"""
        self.client.force_authenticate(user=self.admin)
        new_officer = User.objects.create_user(
            username='officer2',
            password='pass123',
            role='OFFICER'
        )
        data = {'officer_ids': [new_officer.id]}
        response = self.client.post(f'/api/departments/{self.department.id}/officers/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.department.officers.count(), 2)
    
    def test_department_hierarchy(self):
        """Test department hierarchy tree"""
        self.client.force_authenticate(user=self.admin)
        
        # Create hierarchy
        parent = Department.objects.create(
            name='Parent Dept',
            code='PAR001',
            department_type='FACULTY'
        )
        child = Department.objects.create(
            name='Child Dept',
            code='CHI001',
            department_type='ICT',
            parent_department=parent
        )
        
        response = self.client.get('/api/departments/hierarchy/tree/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
