from django.urls import path
from .views import upload_csv, home, StudentListView, AttendanceListView, AttendanceDetailView

urlpatterns = [
    path('', home, name='home'),  # Home API
    path('students/', StudentListView.as_view(), name='students_list'),  # Fetch students
    path('attendance/', AttendanceListView.as_view(), name='attendance_list_create'),  # List & create attendance
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance_detail'),  # Retrieve, update, delete
    path('upload-csv/', upload_csv, name='upload_csv'),  # Upload attendance via CSV
]


