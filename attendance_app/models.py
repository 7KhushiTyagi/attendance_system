from django.db import models
import csv
from django.core.exceptions import ValidationError

class Student(models.Model):
    reg_no = models.CharField(max_length=20, unique=True)  # Student's registration number
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reg_no} - {self.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)  # Linking Attendance to Student
    date = models.DateField()  # Date of attendance
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Absent')

    class Meta:
        unique_together = ('student', 'date')  # Prevent duplicate attendance records

    def __str__(self):
        return f"{self.student.reg_no} - {self.date} - {self.status}"

def import_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                student, created = Student.objects.get_or_create(
                    reg_no=row['reg_no'],
                    defaults={'name': row['name']}
                )
                Attendance.objects.create(
                    student=student,
                    date=row['date'],
                    status=row['status']
                )
            except ValidationError as e:
                print(f"Error importing row {row}: {e}")
