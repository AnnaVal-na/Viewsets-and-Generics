from django.http import JsonResponse
from django.views import View

class RootView(View):
    def get(self, request):
        return JsonResponse({
            "message": "LMS API is running",
            "endpoints": {
                "admin": "/admin/",
                "api": "/api/",
                "swagger": "/swagger/",
                "redoc": "/redoc/"
            }
        })
