from rest_framework import serializers
from .models import Attendance, Student

class AttendanceSerializer(serializers.ModelSerializer):
    student_reg_no = serializers.CharField(write_only=True)  # Accepts reg_no from CSV

    class Meta:
        model = Attendance
        fields = ['student_reg_no', 'date', 'status']

    def create(self, validated_data):
        reg_no = validated_data.pop('student_reg_no')
        student = Student.objects.filter(reg_no=reg_no).first()

        if not student:
            raise serializers.ValidationError({"student_reg_no": "Student with this reg_no does not exist."})

        attendance = Attendance.objects.create(student=student, **validated_data)
        return attendance
    
    

