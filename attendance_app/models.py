from django.db import models

class Student(models.Model):
    reg_no = models.CharField(max_length=20, unique=True)  # Student's registration number
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reg_no} - {self.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True,blank=True)  # Linking Attendance to Student
    date = models.DateField()  # Date of attendance
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.reg_no} - {self.date} - {self.status}"


