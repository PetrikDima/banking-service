from django.contrib import admin

from user_service.models import CustomUser

# Register your models here.
admin.site.register(CustomUser)  # Register the CustomUser model in the admin interface
