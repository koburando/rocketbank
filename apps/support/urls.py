"""
URL configuration for the Support app.
"""

from django.urls import path

from apps.support import views

app_name = "support"

urlpatterns = [
    path("", views.SupportTicketListView.as_view(), name="list"),
    path("faq/", views.FAQListView.as_view(), name="faq"),
    path("create/", views.SupportTicketCreateView.as_view(), name="create"),
    path("<int:pk>/", views.SupportTicketDetailView.as_view(), name="detail"),
]
