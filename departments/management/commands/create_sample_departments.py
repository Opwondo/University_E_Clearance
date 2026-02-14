from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from departments.models import Department

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample department data for testing'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample departments...')
        
        # Create departments by type
        departments_data = [
            # Academic departments
            {'name': 'Faculty of Engineering', 'code': 'ENG001', 'type': 'FACULTY'},
            {'name': 'Faculty of Science', 'code': 'SCI001', 'type': 'FACULTY'},
            {'name': 'Faculty of Arts', 'code': 'ART001', 'type': 'FACULTY'},
            
            # Service departments
            {'name': 'University Library', 'code': 'LIB001', 'type': 'LIBRARY'},
            {'name': 'Finance Office', 'code': 'FIN001', 'type': 'FINANCE'},
            {'name': 'ICT Services', 'code': 'ICT001', 'type': 'ICT'},
            {'name': 'Student Hostels', 'code': 'HOS001', 'type': 'HOSTEL'},
            {'name': 'Sports Department', 'code': 'SPO001', 'type': 'SPORTS'},
            {'name': 'Health Services', 'code': 'HEA001', 'type': 'HEALTH'},
        ]
        
        created_count = 0
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
                created_count += 1
                self.stdout.write(f'  Created: {dept.name}')
        
        # Get or create officers
        officers = User.objects.filter(role='OFFICER')
        if officers.exists():
            for dept in Department.objects.all():
                dept.officers.add(*officers[:2])
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} departments')
        )
