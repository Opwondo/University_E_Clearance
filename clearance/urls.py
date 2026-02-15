from django.urls import path
from . import views

urlpatterns = [
    # Workflow endpoints
    path('workflows/', views.WorkflowListView.as_view(), name='workflow-list'),
    
    # Session endpoints
    path('sessions/', views.ClearanceSessionListCreateView.as_view(), name='session-list'),
    path('sessions/<int:pk>/', views.ClearanceSessionDetailView.as_view(), name='session-detail'),
    
    # Student summary
    path('student/summary/', views.StudentClearanceSummaryView.as_view(), name='student-summary'),
    
    # Officer pending clearances
    path('pending/', views.PendingClearancesView.as_view(), name='pending-clearances'),
    
    # Record endpoints
    path('records/<int:pk>/', views.ClearanceRecordDetailView.as_view(), name='record-detail'),
    path('records/<int:pk>/approve/', views.ApproveClearanceView.as_view(), name='approve-clearance'),
    path('records/<int:pk>/reject/', views.RejectClearanceView.as_view(), name='reject-clearance'),
    
    # Comment endpoints
    path('records/<int:record_id>/comments/', views.ClearanceCommentsView.as_view(), name='record-comments'),
]
