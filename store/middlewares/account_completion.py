from django.shortcuts import redirect


class AccountCompletionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            # User already has email → normal operation
            if request.user.email:
                return self.get_response(request)

            allowed_paths = [
                "/complete-account/",
                "/complete-account/verify/",
                "/logout/",
            ]

            # Allow account completion URLs
            if request.path in allowed_paths:
                return self.get_response(request)

            # Allow Django admin
            if request.path.startswith("/admin/"):
                return self.get_response(request)

            return redirect("complete_account")

        return self.get_response(request)