"""
URL configuration for the Credits app.
"""

from django.urls import path

from apps.credits import views

app_name = "credits"

urlpatterns = [
    path("", views.LoanListView.as_view(), name="list"),
    path("catalog/", views.CreditProductListView.as_view(), name="catalog"),
    path("catalog/<slug:slug>/", views.CreditProductDetailView.as_view(), name="detail"),
    path("calculator/", views.LoanCalculatorView.as_view(), name="calculator"),
    path("apply/", views.LoanApplyCreateView.as_view(), name="apply"),
]
