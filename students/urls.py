from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentProfileListCreateView.as_view(), name='student-list'),
    path('<int:pk>/', views.StudentProfileDetailView.as_view(), name='student-detail'),
    path('me/profile/', views.CurrentStudentProfileView.as_view(), name='current-student-profile'),
]
