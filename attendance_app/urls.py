from django.urls import path
from .views import upload_excel, delete_sheet

urlpatterns = [
    path('upload-excel/', upload_excel, name='upload_excel'),  # Upload attendance via Excel
    path('delete-sheet/', delete_sheet, name='delete_sheet'),  # Delete attendance records by sheet name
]
