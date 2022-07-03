from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
    )
    list_display_links = ("id",)
    list_per_page = 50

admin.site.register(User, UserAdmin)

