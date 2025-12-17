from django.utils import timezone  # ✅ FIXED: Correct import
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Attendee
import json

def index(request):
    """Render the QR scanner page."""
    return render(request, 'scanner/index.html')

@require_http_methods(["POST"])
@csrf_exempt
def scan_qr(request):
    """
    Handle QR scan and mark attendance.
    Expects JSON with registration_number field.
    """
    try:
        # ✅ FIXED: Handle both JSON and POST data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            reg_no = data.get('registration_number', '').strip()
        else:
            reg_no = request.POST.get('registration_number', '').strip()
        
        if not reg_no:
            return JsonResponse({
                "status": "invalid_qr",
                "message": "QR code could not be read"
            }, status=400)
        
        # Check if attendee exists in database
        try:
            attendee = Attendee.objects.get(registration_number=reg_no)
        except Attendee.DoesNotExist:
            return JsonResponse({
                "status": "not_registered",
                "message": f"Registration #{reg_no} not found in database"
            }, status=404)
        
        # Check if already marked attendance
        if attendee.attended:
            return JsonResponse({
                "status": "already_marked",
                "name": attendee.name,
                "message": f"⚠️ {attendee.name} - Attendance already marked!"
            }, status=200)
        
        # Mark attendance
        attendee.attended = True
        attendee.checked_in_at = timezone.now()
        attendee.save()
        
        return JsonResponse({
            "status": "success",
            "name": attendee.name,
            "message": f"✅ {attendee.name} - Attendance marked successfully!"
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            "status": "invalid_json",
            "message": "Invalid data format"
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

def scanner_page(request):
    """Render scanner page."""
    return render(request, "scanner/index.html")
