from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from store.models.address import SavedAddress


@login_required
def edit_address(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False})

    try:
        data = json.loads(request.body)
        addr = SavedAddress.objects.get(id=id, user=request.user)

        addr.full_name = data.get("name")
        addr.phone = data.get("phone")
        addr.pincode = data.get("pincode")
        addr.address = data.get("address")
        addr.save()

        return JsonResponse({"success": True})
    except Exception as e:
        
        return JsonResponse({"success": False})


@login_required
def delete_address(request, id):
    try:
        addr = SavedAddress.objects.get(id=id, user=request.user)
        addr.delete()
        return JsonResponse({"success": True})
    except Exception as e:
   
        return JsonResponse({"success": False})
