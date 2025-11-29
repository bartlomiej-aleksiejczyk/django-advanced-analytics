from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomizedUser, FailedLogin


admin.site.register(CustomizedUser, UserAdmin)
admin.site.register(FailedLogin)