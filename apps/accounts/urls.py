"""
URL configuration for the Accounts app.
"""

from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("", views.BankAccountListView.as_view(), name="list"),
    path("open/", views.OpenAccountCreateView.as_view(), name="open"),
    path("beneficiaries/", views.BeneficiaryFormsetView.as_view(), name="beneficiaries"),
    path(
        "beneficiaries/<int:pk>/delete/",
        views.BeneficiaryDeleteView.as_view(),
        name="beneficiary-delete",
    ),
    path("<uuid:pk>/", views.BankAccountDetailView.as_view(), name="detail"),
    path("iban/<iban:iban>/", views.AccountByIbanDetailView.as_view(), name="detail-by-iban"),
]
