"""
URL configuration for the Users app.
"""

from django.urls import path

from apps.users import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify-email/<str:token>/", views.VerifyEmailView.as_view(), name="verify-email"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("logout/", views.LogoutUserView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("security/", views.SecuritySettingsView.as_view(), name="security"),
    path("password-change/", views.UserPasswordChangeView.as_view(), name="password-change"),
    path("kyc-upload/", views.KYCUploadView.as_view(), name="kyc-upload"),
    path("password-reset/", views.CustomPasswordResetView.as_view(), name="password-reset"),
    path(
        "password-reset/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset/complete/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password-reset-complete",
    ),
]
