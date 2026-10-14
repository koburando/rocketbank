"""
Django admin configuration for the Users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import LoginAudit, Profile, User, UserFavorite


class ProfileInline(admin.StackedInline):
    """Inline profile editor within user admin."""

    model = Profile
    can_delete = False
    verbose_name_plural = "profile"
    fk_name = "user"
    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "avatar",
                    "birth_date",
                    "address",
                )
            },
        ),
        (
            "Verification & Preferences",
            {
                "fields": (
                    "kyc_status",
                    "preferred_theme",
                    "preferred_language",
                )
            },
        ),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with profile inline and UUID display."""

    inlines = [ProfileInline]
    list_display = (
        "email",
        "username",
        "phone_number",
        "is_verified",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = (
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    search_fields = ("email", "username", "phone_number")
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"
    readonly_fields = ("id", "date_joined", "last_login")
    list_editable = ("is_verified",)

    fieldsets = (
        (None, {"fields": ("id", "email", "username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for Profile model."""

    list_display = (
        "user",
        "kyc_status",
        "preferred_theme",
        "preferred_language",
        "birth_date",
        "created_at",
    )
    list_filter = ("kyc_status", "preferred_theme")
    search_fields = ("user__email", "user__username")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user",)

    fieldsets = (
        (None, {"fields": ("user",)}),
        (
            "Personal",
            {"fields": ("avatar", "birth_date", "address")},
        ),
        (
            "Verification",
            {"fields": ("kyc_status",)},
        ),
        (
            "Preferences",
            {
                "fields": (
                    "preferred_theme",
                    "preferred_language",
                )
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


@admin.register(LoginAudit)
class LoginAuditAdmin(admin.ModelAdmin):
    """Admin for login audit trail."""

    list_display = (
        "user",
        "ip_address",
        "login_successful",
        "location",
        "created_at",
    )
    list_filter = ("login_successful", "created_at")
    search_fields = (
        "user__email",
        "ip_address",
        "location",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "user",
        "ip_address",
        "user_agent",
        "login_successful",
        "location",
        "created_at",
    )


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    """Admin for user favorites."""

    list_display = ("user", "item_type", "item_id", "created_at")
    list_filter = ("item_type", "created_at")
    search_fields = ("user__email", "item_id")
    readonly_fields = ("created_at", "updated_at")
