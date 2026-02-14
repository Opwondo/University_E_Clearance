from django.urls import path
from . import views

urlpatterns = [
    # Department CRUD
    path('', views.DepartmentListCreateView.as_view(), name='department-list'),
    path('<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    
    # Department officers management
    path('<int:pk>/officers/', views.DepartmentOfficersView.as_view(), name='department-officers'),
    
    # Department hierarchy
    path('hierarchy/tree/', views.DepartmentHierarchyView.as_view(), name='department-hierarchy'),
]
