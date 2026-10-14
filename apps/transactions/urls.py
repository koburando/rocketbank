"""
URL configuration for the Transactions app.
"""

from django.urls import path

from apps.transactions import views

app_name = "transactions"

urlpatterns = [
    path("", views.TransactionListView.as_view(), name="list"),
    path("transfer/", views.MoneyTransferView.as_view(), name="transfer"),
    path("<ref:reference_number>/", views.TransactionDetailView.as_view(), name="receipt"),
]
