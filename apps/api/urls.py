"""
URL Configuration for RocketBank REST API v1.
Registers ViewSets via DefaultRouter and wires SimpleJWT authentication.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.api.views import (
    BankAccountViewSet,
    BankCardViewSet,
    CardProductViewSet,
    DepositProductViewSet,
    FavoritesViewSet,
    LoanApplicationViewSet,
    LoanProductViewSet,
    MonthlyAnalyticsViewSet,
    NotificationViewSet,
    ProductReviewViewSet,
    SavingGoalViewSet,
    TransactionViewSet,
    UserDepositViewSet,
    UserProfileViewSet,
)

app_name = "api_v1"

router = DefaultRouter()
router.register(r"accounts", BankAccountViewSet, basename="account")
router.register(r"cards", BankCardViewSet, basename="card")
router.register(r"card-products", CardProductViewSet, basename="card-product")
router.register(r"transactions", TransactionViewSet, basename="transaction")
router.register(r"loans", LoanApplicationViewSet, basename="loan")
router.register(r"loan-products", LoanProductViewSet, basename="loan-product")
router.register(r"deposits", UserDepositViewSet, basename="deposit")
router.register(r"deposit-products", DepositProductViewSet, basename="deposit-product")
router.register(r"saving-goals", SavingGoalViewSet, basename="saving-goal")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"reviews", ProductReviewViewSet, basename="review")
router.register(r"analytics/monthly-summary", MonthlyAnalyticsViewSet, basename="monthly-summary")
router.register(r"favorites", FavoritesViewSet, basename="favorite")
router.register(r"profile", UserProfileViewSet, basename="profile")

urlpatterns = [
    # JWT Authentication Endpoints
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "auth/profile/",
        UserProfileViewSet.as_view({"get": "list", "patch": "partial_update"}),
        name="auth_profile",
    ),
    # Router Endpoints
    path("", include(router.urls)),
]
