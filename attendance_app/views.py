import csv
import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance, Student
from .serializers import AttendanceSerializer
from django.http import JsonResponse

@api_view(['POST'])
def upload_csv(request):
    """ API to upload attendance via CSV """
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    try:
        decoded_file = file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)

        next(reader, None)  # Skip header row
        records = []

        for row in reader:
            if len(row) != 3:
                return Response({"error": "CSV format should have 3 columns: reg_no, date, status"}, status=status.HTTP_400_BAD_REQUEST)

            reg_no, date, status_value = row

            student = Student.objects.filter(reg_no=reg_no).first()
            if not student:
                return Response({"error": f"Student with reg_no {reg_no} not found"}, status=status.HTTP_400_BAD_REQUEST)

            attendance_data = {
                "student_reg_no": reg_no,
                "date": date,
                "status": status_value
            }

            serializer = AttendanceSerializer(data=attendance_data)
            if serializer.is_valid():
                records.append(serializer.save())
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"{len(records)} records uploaded successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



def home(request):
    return JsonResponse({"message": "Welcome to the Attendance System API!"})
