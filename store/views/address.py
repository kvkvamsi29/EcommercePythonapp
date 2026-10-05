from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from store.models.address import SavedAddress



def delete_address(request, id):
    if request.method == "POST":
        try:
            SavedAddress.objects.filter(id=id).delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


def edit_address(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            address = SavedAddress.objects.get(id=id)

            address.full_name = data["name"]
            address.phone = data["phone"]
            address.pincode = data["pincode"]
            address.address = data["address"]
            address.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})
