from django.contrib import admin
from authentication.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "pk")


admin.site.register(User, UserAdmin)
