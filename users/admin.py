from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = [
        "full_name",
    ]
    list_display = (
        "id",
        "full_name",
        "phone_number",
    )
    readonly_fields = ("last_login",)
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                    "full_name",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "full_name",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
