from urllib import request
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST  # Restrict to POST requests
from .models import Student, Attendance
from .forms import ExcelUploadForm

@csrf_exempt  # Disable CSRF for API calls
@require_POST  # Ensure only POST requests are allowed
def upload_excel(request):
    print("Received POST request")  # Debugging step
    print("FILES: ", request.FILES)  # Check if file is received

    if 'file' not in request.FILES:
        return JsonResponse({"error": "No file uploaded. Make sure to send a file with key 'file'."}, status=400)

    form = ExcelUploadForm(request.POST, request.FILES)
    
    if not form.is_valid():
        return JsonResponse({"error": "Invalid form submission. Please upload a valid Excel file."}, status=400)

    file = request.FILES['file']

    try:
        # Read the Excel file
        df = pd.read_excel(file, engine='openpyxl')

        # Ensure required columns are present
        required_columns = ['ParticipantId', 'Participant Name', 'Session Attended (P/A)']
        if not all(col in df.columns for col in required_columns):
            return JsonResponse({"error": "Invalid file format. Please upload the correct Excel sheet."}, status=400)

        errors = []
        success_count = 0

        # Get sheet name from user input
        sheet_name = request.POST.get("sheet_name", "Default Sheet")

        # Process each row
        for index, row in df.iterrows():
            reg_no = str(row.get('ParticipantId', '')).strip()
            name = str(row.get('Participant Name', '')).strip()
            status = str(row.get('Session Attended (P/A)', '')).strip()

            # Validate data
            if not reg_no or not name:
                errors.append(f"Missing Participant ID or Name at row {index + 2}. Skipping entry.")
                continue
            
            if status not in ['P', 'A']:
                errors.append(f"Invalid attendance value at row {index + 2}. Use 'P' or 'A'.")
                continue

            # Get or create student
            student, _ = Student.objects.get_or_create(registration_number=reg_no, defaults={'name': name})

            # Save attendance
            Attendance.objects.create(student=student, status=status, sheet_name=sheet_name)
            success_count += 1

        return JsonResponse({
            "message": f"Attendance data uploaded successfully. {success_count} records saved.",
            "sheet_name": sheet_name,  # Include sheet name in response
            "errors": errors
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Error processing file: {str(e)}"}, status=500)

@csrf_exempt
@require_POST
def delete_sheet(request):
    """Delete attendance records for a given sheet name."""
    try:
        data = request.POST
        sheet_name = data.get("sheet_name", "").strip()

        if not sheet_name:
            return JsonResponse({"error": "Sheet name is required."}, status=400)

        deleted_count, _ = Attendance.objects.filter(sheet_name=sheet_name).delete()

        if deleted_count == 0:
            return JsonResponse({"error": "No records found for the given sheet name."}, status=404)

        return JsonResponse({"message": f"Sheet '{sheet_name}' deleted successfully.", "deleted_records": deleted_count}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
