"""
Views for the Notifications app: Notifications Center and Mark as Read FBVs.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from apps.notifications.models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    """
    Notifications Center (Screen 15).
    """

    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user).order_by("-created_at")
        filter_type = self.request.GET.get("type")
        if filter_type:
            qs = qs.filter(notification_type=filter_type)
        if self.request.GET.get("unread") == "1":
            qs = qs.filter(is_read=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unread_total"] = Notification.objects.filter(
            user=self.request.user, is_read=False
        ).count()
        return context


@login_required
@require_POST
def mark_notification_as_read(request, pk):
    """
    Function-Based View (FBV) with @require_POST and @login_required (Section 7).
    Marks a specific notification as read.
    """
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.mark_as_read()
    messages.success(request, f"Marked '{notif.title}' as read.")
    return redirect(request.META.get("HTTP_REFERER") or reverse("notifications:list"))


@login_required
@require_POST
def mark_all_notifications_as_read(request):
    """
    Function-Based View (FBV) to mark all user notifications as read at once.
    """
    Notification.objects.filter(user=request.user, is_read=False).update(
        is_read=True, read_at=timezone.now()
    )
    messages.success(request, "All notifications marked as read.")
    return redirect("notifications:list")
