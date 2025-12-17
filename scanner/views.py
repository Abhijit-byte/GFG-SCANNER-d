from django.utils import timezone  # ✅ CORRECT import
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
    Expects: POST data with registration_number field
    """
    try:
        # Get registration number from POST data
        reg_no = request.POST.get("registration_number", "").strip()
        
        if not reg_no:
            return JsonResponse({
                "status": "invalid_qr",
                "message": "QR code could not be read"
            }, status=400)
        
        print(f"[DEBUG] Scanning registration: {reg_no}")  # Debug log
        
        # Check if attendee exists
        try:
            attendee = Attendee.objects.get(registration_number=reg_no)
            print(f"[DEBUG] Found: {attendee.name}, Attended: {attendee.attended}")
        except Attendee.DoesNotExist:
            print(f"[DEBUG] Not found in database")
            return JsonResponse({
                "status": "not_registered",
                "message": f"Registration #{reg_no} not found"
            }, status=404)
        
        # Check if already marked
        if attendee.attended:
            print(f"[DEBUG] Already marked")
            return JsonResponse({
                "status": "already_marked",
                "name": attendee.name,
                "message": f"{attendee.name} - Already marked"
            }, status=200)
        
        # Mark attendance
        attendee.attended = True
        attendee.checked_in_at = timezone.now()
        attendee.save()
        
        print(f"[DEBUG] Attendance marked for {attendee.name}")
        return JsonResponse({
            "status": "success",
            "name": attendee.name,
            "message": f"{attendee.name} - Attendance marked"
        }, status=200)
    
    except Exception as e:
        print(f"[DEBUG] Error: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

def scanner_page(request):
    """Render scanner page."""
    return render(request, "scanner/index.html")
