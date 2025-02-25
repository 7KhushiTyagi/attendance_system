from rest_framework import serializers
from .models import Attendance, Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['reg_no', 'name']

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())  # Use student ID instead of reg_no

    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']

    def validate(self, data):
        """ Ensure a student does not have duplicate attendance for the same date """
        student = data.get('student')
        date = data.get('date')

        if Attendance.objects.filter(student=student, date=date).exists():
            raise serializers.ValidationError({"error": "Attendance for this student on this date already exists."})

        return data

