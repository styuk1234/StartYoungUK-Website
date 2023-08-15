import os
from django.http import HttpResponse
from django.conf import settings

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def is_admin_page(self, request):
        return request.path.startswith(f"/{os.getenv('ADMIN_URL')}")
    
    
    def __call__(self, request):
        response = self.get_response(request)

        if not settings.DEBUG and settings.SITE_UNDER_MAINTENANCE and not self.is_admin_page(request):
            maintenance_banner = """
                <div style="background-color: red; color: white; padding: 10px; text-align: center; z-index: 9999; position: fixed; top:0; left:0; width:100%; ">
                SITE UNDER MAINTENANCE, PLEASE DO NOT PERFORM ANY ACTIVITIES ON THIS WEBSITE TILL THIS BANNER IS GONE!
            </div>           
            """
            response.content = maintenance_banner.encode() + response.content

        return response