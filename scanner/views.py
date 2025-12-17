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
    if request.method != "POST":
        return JsonResponse({"status": "method_not_allowed"}, status=405)

    reg_no = request.POST.get("registration_number")

    if not reg_no:
        return JsonResponse({"status": "invalid_qr"}, status=400)

    try:
        attendee = Attendee.objects.get(registration_number=reg_no)

        if attendee.attended:
            return JsonResponse({
                "status": "already_marked",
                "name": attendee.name
            })

        attendee.attended = True
        attendee.checked_in_at = timezone.now()
        attendee.save(update_fields=["attended", "checked_in_at"])

        return JsonResponse({
            "status": "success",
            "name": attendee.name
        })

    except Attendee.DoesNotExist:
        return JsonResponse({
            "status": "not_registered"
        }, status=404)
