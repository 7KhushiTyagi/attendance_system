from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django import forms
from django.shortcuts import redirect
import csv
import io
from .models import Attendance, Student

class CSVUploadForm(forms.Form):
    file = forms.FileField()

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("get_reg_no", "get_name", "date", "status")  # Fix: Use helper methods
    list_filter = ('status', 'date')  
    search_fields = ('student__reg_no', 'student__name')  # Fix: Search inside Student model

    def get_reg_no(self, obj):
        return obj.student.reg_no  # Fetch reg_no from Student
    get_reg_no.admin_order_field = 'student__reg_no'  
    get_reg_no.short_description = 'Reg No'

    def get_name(self, obj):
        return obj.student.name  # Fetch name from Student
    get_name.admin_order_field = 'student__name'  
    get_name.short_description = 'Name'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.admin_site.admin_view(self.upload_csv_view), name="upload_csv"),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        """Handles CSV upload inside Django Admin."""
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"]

                # Read and process CSV
                decoded_file = file.read().decode("utf-8")
                io_string = io.StringIO(decoded_file)
                reader = csv.reader(io_string)
                
                next(reader, None)  # Skip header row
                for row in reader:
                    reg_no, name, status = row  # Ensure CSV has these 3 columns
                    
                    # Get or create Student record
                    student, _ = Student.objects.get_or_create(reg_no=reg_no, defaults={"name": name})

                    # Create Attendance record
                    Attendance.objects.create(
                        student=student,
                        status=status
                    )

                self.message_user(request, "CSV uploaded successfully!")
                return redirect("..")  # Redirect back to admin panel

        else:
            form = CSVUploadForm()

        context = {"form": form}
        return TemplateResponse(request, "admin/upload_csv.html", context)

admin.site.register(Attendance, AttendanceAdmin)

