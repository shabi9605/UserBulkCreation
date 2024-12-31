from django.contrib import admin
from .models import User, BulkUploadLogs
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "age"]


admin.site.register(BulkUploadLogs)