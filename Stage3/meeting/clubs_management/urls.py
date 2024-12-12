from django.urls import path
from . import views

urlpatterns = [
    path('meetings/', views.meeting_list, name='meeting_list'),
    path('meetings/new/', views.meeting_edit, name='meeting_create'),
    path('meetings/edit/<int:meeting_id>/', views.meeting_edit, name='meeting_edit'),
    path('meetings/delete/<int:meeting_id>/', views.meeting_delete, name='meeting_delete'),
    path('meetings/report/', views.meeting_report, name='meeting_report'),
    path('', views.meeting_list, name='meeting_list'),
]
