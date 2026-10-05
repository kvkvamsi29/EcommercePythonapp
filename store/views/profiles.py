from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models.profiles import UserProfile

@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST["phone"]
        profile.address_line = request.POST["address"]
        profile.city = request.POST["city"]
        profile.state = request.POST["state"]
        profile.pincode = request.POST["pincode"]
        profile.save()
        return redirect("profile")

    return render(request, "store/profile.html", {"profile": profile})
