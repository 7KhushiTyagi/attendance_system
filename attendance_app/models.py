from django.db import models
from django.core.exceptions import ValidationError

class Student(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.registration_number} - {self.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])
    sheet_name = models.CharField(max_length=100, default="Untitled Sheet")

    class Meta:
        unique_together = ('student', 'date', 'sheet_name')

    def clean(self):
        self.status = self.normalize_status(self.status)
        if self.status is None:
            raise ValidationError("Invalid attendance status. Use 'P', 'A', 'present', or 'absent'.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @staticmethod
    def normalize_status(value):
        if not isinstance(value, str):
            return None
        value = value.strip().lower()
        if value in ["p", "present"]:
            return "P"
        elif value in ["a", "absent"]:
            return "A"
        return None

    def __str__(self):
        return f"{self.student.name} - {self.status} ({self.sheet_name})"
