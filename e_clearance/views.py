from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_root(request):
    """
    API root endpoint showing available services
    """
    return JsonResponse({
        "name": "University E-Clearance System API",
        "version": "2.0.0",
        "status": "operational",
        "documentation": {
            "admin": "/admin/",
            "api_root": "/api/",
            "api_docs": "https://github.com/Opwondo/University_E_Clearance#api-documentation",
            "dashboard": "/api/reports/dashboard/"
        },
        "endpoints": {
            "authentication": {
                "login": "/api/auth/login/",
                "refresh": "/api/auth/refresh/"
            },
            "students": "/api/students/",
            "departments": "/api/departments/",
            "clearance": "/api/clearance/",
            "audit": "/api/audit/",
            "reports": "/api/reports/",
            "certificates": "/api/certificates/"
        },
        "message": "Welcome to the University E-Clearance System API. Please use the appropriate endpoints."
    })
