"""
URL configuration for the Deposits app.
"""

from django.urls import path

from apps.deposits import views

app_name = "deposits"

urlpatterns = [
    path("", views.DepositListView.as_view(), name="list"),
    path("catalog/", views.DepositProductListView.as_view(), name="catalog"),
    path("open/", views.OpenDepositCreateView.as_view(), name="open"),
]
