"""
URL configuration for the Notifications app.
"""

from django.urls import path

from apps.notifications import views

app_name = "notifications"

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="list"),
    path("<int:pk>/read/", views.mark_notification_as_read, name="mark-read"),
    path("read-all/", views.mark_all_notifications_as_read, name="read-all"),
]
