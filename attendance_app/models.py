from django.db import models
from django.core.exceptions import ValidationError

class Student(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.registration_number} - {self.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)

    date = models.DateField(auto_now_add=True)  # Change as per requirement
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])

    class Meta:
        unique_together = ('student', 'date')  # Prevent duplicate attendance records

    def clean(self):
        """Normalize status input before validation"""
        self.status = self.normalize_status(self.status)
        if self.status is None:
            raise ValidationError("Invalid attendance status. Use 'P', 'A', 'present', or 'absent'.")

    def save(self, *args, **kwargs):
        """Override save method to normalize status before saving"""
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    @staticmethod
    def normalize_status(value):
        """Convert various inputs to 'P' or 'A'"""
        value = value.strip().lower()  # Remove spaces and make lowercase
        if value in ["p", "present"]:
            return "P"
        elif value in ["a", "absent"]:
            return "A"
        return None  # Invalid value

    def __str__(self):
        return f"{self.student.name} - {self.status}"


