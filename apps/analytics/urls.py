"""
URL configuration for the Analytics app.
"""

from django.urls import path

from apps.analytics import views

app_name = "analytics"

urlpatterns = [
    path("", views.AnalyticsDashboardView.as_view(), name="dashboard"),
    path("goals/", views.AnalyticsDashboardView.as_view(), name="goals"),
    path("goals/<int:pk>/delete/", views.SavingGoalDeleteView.as_view(), name="goal-delete"),
]
