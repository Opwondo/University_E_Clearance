from django.db import migrations

def create_graduation_workflow(apps, schema_editor):
    ClearanceWorkflow = apps.get_model('clearance', 'ClearanceWorkflow')
    WorkflowStage = apps.get_model('clearance', 'WorkflowStage')
    WorkflowStageDepartment = apps.get_model('clearance', 'WorkflowStageDepartment')
    Department = apps.get_model('departments', 'Department')
    
    # Create Graduation Workflow
    workflow, created = ClearanceWorkflow.objects.get_or_create(
        session_type='GRADUATION',
        defaults={
            'name': 'Graduation Clearance',
            'description': 'Standard graduation clearance process for final year students',
            'is_active': True
        }
    )
    
    if created:
        # Stage 1: Academic Clearance
        stage1 = WorkflowStage.objects.create(
            workflow=workflow,
            name='Academic Clearance',
            stage_order=1,
            description='Clearance from academic units'
        )
        
        # Stage 2: Financial Clearance
        stage2 = WorkflowStage.objects.create(
            workflow=workflow,
            name='Financial Clearance',
            stage_order=2,
            description='Clear all financial obligations'
        )
        
        # Stage 3: Administrative Clearance
        stage3 = WorkflowStage.objects.create(
            workflow=workflow,
            name='Administrative Clearance',
            stage_order=3,
            description='Clearance from administrative units'
        )
        
        # Stage 4: Final Clearance
        stage4 = WorkflowStage.objects.create(
            workflow=workflow,
            name='Final Clearance',
            stage_order=4,
            description='Final approval and graduation processing'
        )
        
        # Try to assign departments if they exist
        try:
            # Get departments (they might not exist yet, so we use get_or_create logic)
            library, _ = Department.objects.get_or_create(
                code='LIB001',
                defaults={
                    'name': 'University Library',
                    'department_type': 'LIBRARY'
                }
            )
            
            finance, _ = Department.objects.get_or_create(
                code='FIN001',
                defaults={
                    'name': 'Finance Office',
                    'department_type': 'FINANCE'
                }
            )
            
            hostel, _ = Department.objects.get_or_create(
                code='HOS001',
                defaults={
                    'name': 'Student Hostels',
                    'department_type': 'HOSTEL'
                }
            )
            
            ict, _ = Department.objects.get_or_create(
                code='ICT001',
                defaults={
                    'name': 'ICT Services',
                    'department_type': 'ICT'
                }
            )
            
            faculty, _ = Department.objects.get_or_create(
                code='FAC001',
                defaults={
                    'name': 'Faculty Office',
                    'department_type': 'FACULTY'
                }
            )
            
            registrar, _ = Department.objects.get_or_create(
                code='REG001',
                defaults={
                    'name': 'Academic Registrar',
                    'department_type': 'FACULTY'
                }
            )
            
            # Assign departments to stages
            # Stage 1: Academic Clearance
            WorkflowStageDepartment.objects.create(
                stage=stage1,
                department=faculty,
                order_within_stage=1,
                is_mandatory=True
            )
            
            # Stage 2: Financial Clearance (can be parallel - order=0)
            WorkflowStageDepartment.objects.create(
                stage=stage2,
                department=finance,
                order_within_stage=0,
                is_mandatory=True
            )
            
            WorkflowStageDepartment.objects.create(
                stage=stage2,
                department=library,
                order_within_stage=0,
                is_mandatory=True
            )
            
            WorkflowStageDepartment.objects.create(
                stage=stage2,
                department=hostel,
                order_within_stage=0,
                is_mandatory=True
            )
            
            # Stage 3: Administrative Clearance
            WorkflowStageDepartment.objects.create(
                stage=stage3,
                department=ict,
                order_within_stage=0,
                is_mandatory=True
            )
            
            # Stage 4: Final Clearance
            WorkflowStageDepartment.objects.create(
                stage=stage4,
                department=registrar,
                order_within_stage=1,
                is_mandatory=True
            )
            
        except Exception as e:
            # Log the error but don't fail the migration
            print(f"Warning: Could not assign departments to workflow: {e}")

def reverse_func(apps, schema_editor):
    ClearanceWorkflow = apps.get_model('clearance', 'ClearanceWorkflow')
    ClearanceWorkflow.objects.filter(session_type='GRADUATION').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('clearance', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(create_graduation_workflow, reverse_func),
    ]
