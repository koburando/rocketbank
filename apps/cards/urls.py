"""
URL configuration for the Cards app.
"""

from django.urls import path

from apps.cards import views

app_name = "cards"

urlpatterns = [
    path("", views.CardListView.as_view(), name="list"),
    path("catalog/", views.CardProductListView.as_view(), name="catalog"),
    path("catalog/<slug:slug>/", views.CardProductDetailView.as_view(), name="detail"),
    path("apply/", views.CardApplyWizardView.as_view(), name="apply"),
    path("<int:pk>/toggle-freeze/", views.toggle_card_freeze, name="toggle-freeze"),
]
