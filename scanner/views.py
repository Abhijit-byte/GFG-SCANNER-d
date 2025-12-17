from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Attendee

import json

def index(request):
    """Render the QR scanner page."""
    return render(request, 'scanner/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def scan_qr(request):
    """Handle QR scan data."""
    try:
        data = json.loads(request.body)
        qr_data = data.get('qr_data')
        
        if not qr_data:
            return JsonResponse({'error': 'No QR data provided'}, status=400)
        
        # Save to database
        qr_scan = Attendee.objects.create(qr_data=qr_data)
        
        return JsonResponse({
            'success': True,
            'message': 'QR code scanned successfully',
            'data': qr_data,
            'id': qr_scan.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
