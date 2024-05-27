from django.shortcuts import redirect
from django.urls import reverse
from .models import Employee

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if 'login' in  request.path or 'register' in  request.path :
                return redirect('dashboard')
        response = self.get_response(request)
        return response
