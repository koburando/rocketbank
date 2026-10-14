"""
Reusable Class-Based View mixins for RocketBank.
"""

import json

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


class OwnerRequiredMixin:
    """
    Mixin that ensures the requested object belongs to the authenticated user.
    Raises PermissionDenied (403) if the object does not belong to request.user.
    """

    owner_field = "owner"

    def get_owner_field(self):
        return self.owner_field

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        field = self.get_owner_field()

        # Check either specified owner_field or fallback to user/owner
        owner = getattr(obj, field, None)
        if owner is None and hasattr(obj, "user"):
            owner = getattr(obj, "user")
        elif owner is None and hasattr(obj, "owner"):
            owner = getattr(obj, "owner")

        if owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to access this resource.")
        return obj


class AjaxResponseMixin:
    """
    Mixin that handles AJAX requests by returning JSON responses.
    """

    def is_ajax(self):
        return self.request.headers.get(
            "x-requested-with"
        ) == "XMLHttpRequest" or "application/json" in self.request.headers.get("accept", "")

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(context, **response_kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.is_ajax():
            errors = json.loads(form.errors.as_json())
            return self.render_to_json_response({"success": False, "errors": errors}, status=400)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_ajax():
            data = {"success": True}
            if hasattr(self, "get_success_url"):
                data["redirect_url"] = self.get_success_url()
            return self.render_to_json_response(data)
        return response


class RoleRequiredMixin:
    """
    Mixin to enforce role or staff requirement for views.
    """

    allowed_roles = []
    require_staff = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.require_staff and not request.user.is_staff:
            raise PermissionDenied("Staff access required.")

        return super().dispatch(request, *args, **kwargs)
