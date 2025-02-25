from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Attendance, Student
from .serializers import AttendanceSerializer, StudentSerializer
import csv
import io

class StudentListView(generics.ListAPIView):
    """ API to list all students """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AttendanceListView(generics.ListCreateAPIView):
    """ API to list attendance records and mark attendance manually """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ API to get, update, or delete a specific attendance record """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
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
        
        header = next(reader, None)  # Read header
        if header != ["reg_no", "date", "status"]:
            return Response({"error": "CSV header format should be: reg_no,date,status"}, status=status.HTTP_400_BAD_REQUEST)

        records = []
        for row in reader:
            print(f"Processing row: {row}")  # Debugging log

            if len(row) != 3:
                return Response({"error": f"Invalid row format: {row}"}, status=status.HTTP_400_BAD_REQUEST)

            reg_no, date, status_value = row
            student = Student.objects.filter(reg_no=reg_no).first()

            if not student:
                print(f"Student with reg_no {reg_no} not found.")  # Debugging log
                continue  

            attendance, created = Attendance.objects.update_or_create(
                student=student, date=date, defaults={"status": status_value}
            )
            records.append(attendance)

        return Response({"message": f"{len(records)} records uploaded successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Error: {e}")  # Debugging log
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def home(request):
    return Response({"message": "Welcome to the Attendance System API!"})
