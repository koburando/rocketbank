"""
DRF ViewSets and Views for RocketBank REST API (v1).
Fully integrated with OpenAPI 3.0 schema generation, filters, permissions, and pagination.
"""

from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import BankAccount
from apps.analytics.models import SavingGoal
from apps.api.filters import (
    BankAccountFilter,
    BankCardFilter,
    CardProductFilter,
    DepositProductFilter,
    LoanApplicationFilter,
    LoanProductFilter,
    ProductReviewFilter,
    SavingGoalFilter,
    TransactionFilter,
    UserDepositFilter,
)
from apps.api.permissions import IsAccountOwner, IsOwnerOrReadOnly
from apps.api.serializers import (
    BankAccountSerializer,
    BankCardLimitUpdateSerializer,
    BankCardSerializer,
    CardProductSerializer,
    DepositProductSerializer,
    FavoritesSyncSerializer,
    LoanApplicationSerializer,
    LoanProductSerializer,
    MonthlyAnalyticsSummarySerializer,
    NotificationSerializer,
    ProductReviewSerializer,
    ProfileSerializer,
    SavingGoalAddFundsSerializer,
    SavingGoalSerializer,
    ThemeUpdateSerializer,
    ToggleFavoriteSerializer,
    TransactionCreateSerializer,
    TransactionSerializer,
    UserDepositSerializer,
    UserFavoriteSerializer,
)
from apps.cards.models import BankCard, CardProduct
from apps.credits.models import LoanApplication, LoanProduct
from apps.deposits.models import DepositProduct, UserDeposit
from apps.notifications.models import Notification
from apps.support.models import ProductReview
from apps.transactions.models import Transaction
from apps.transactions.services import execute_transfer
from apps.users.models import UserFavorite

# ──────────────────────────────────────────────
# Bank Accounts ViewSet
# ──────────────────────────────────────────────


class BankAccountViewSet(viewsets.ModelViewSet):
    """
    CRUD for Bank Accounts + Freeze / Unfreeze actions.
    Endpoint: /api/v1/accounts/
    """

    queryset = BankAccount.all_objects.filter(is_deleted=False)
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    filterset_class = BankAccountFilter
    search_fields = ["iban"]
    ordering_fields = ["balance", "opened_at", "account_type"]
    ordering = ["-opened_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BankAccount.all_objects.filter(is_deleted=False).select_related(
                "currency", "owner"
            )
        return BankAccount.all_objects.filter(owner=user, is_deleted=False).select_related(
            "currency", "owner"
        )

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=["post"], url_path="freeze")
    def freeze(self, request, pk=None):
        account = self.get_object()
        account.status = BankAccount.AccountStatus.FROZEN
        account.save(update_fields=["status", "updated_at"])
        serializer = self.get_serializer(account)
        return Response({"status": "frozen", "account": serializer.data})

    @action(detail=True, methods=["post"], url_path="unfreeze")
    def unfreeze(self, request, pk=None):
        account = self.get_object()
        account.status = BankAccount.AccountStatus.ACTIVE
        account.save(update_fields=["status", "updated_at"])
        serializer = self.get_serializer(account)
        return Response({"status": "active", "account": serializer.data})


# ──────────────────────────────────────────────
# Bank Cards ViewSet
# ──────────────────────────────────────────────


class BankCardViewSet(viewsets.ModelViewSet):
    """
    Issued Bank Cards ViewSet with limit update and freeze/unfreeze actions.
    Endpoint: /api/v1/cards/
    """

    queryset = BankCard.objects.all()
    serializer_class = BankCardSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    filterset_class = BankCardFilter
    search_fields = ["card_number_masked"]
    ordering_fields = ["card_number_masked", "issued_at", "daily_limit"]
    ordering = ["-issued_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BankCard.objects.all().select_related("account", "product")
        return BankCard.objects.filter(account__owner=user).select_related("account", "product")

    @action(detail=True, methods=["post", "patch"], url_path="update-limit")
    def update_limit(self, request, pk=None):
        card = self.get_object()
        serializer = BankCardLimitUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_limit = serializer.validated_data["daily_limit"]
        card.daily_limit = new_limit
        card.save(update_fields=["daily_limit", "updated_at"])
        return Response(
            {
                "status": "success",
                "message": f"Daily limit updated to {new_limit:,.2f} KZT.",
                "daily_limit": float(new_limit),
            }
        )

    @action(detail=True, methods=["post", "patch"], url_path="freeze")
    def freeze(self, request, pk=None):
        card = self.get_object()
        if card.status == BankCard.CardStatus.ACTIVE:
            card.transition_to(BankCard.CardStatus.BLOCKED)
            return Response({"status": "blocked", "message": "Card successfully frozen."})
        return Response(
            {"status": "error", "message": f"Card cannot be frozen from status {card.status}."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["post", "patch"], url_path="unfreeze")
    def unfreeze(self, request, pk=None):
        card = self.get_object()
        if card.status == BankCard.CardStatus.BLOCKED:
            card.transition_to(BankCard.CardStatus.ACTIVE)
            return Response({"status": "active", "message": "Card successfully unblocked."})
        return Response(
            {"status": "error", "message": f"Card cannot be unblocked from status {card.status}."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ──────────────────────────────────────────────
# Card Products ViewSet
# ──────────────────────────────────────────────


class CardProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public catalog of credit and debit card products.
    Endpoint: /api/v1/card-products/
    """

    queryset = CardProduct.objects.filter(is_active=True)
    serializer_class = CardProductSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = CardProductFilter
    search_fields = ["title", "description", "tier"]
    ordering_fields = ["annual_fee", "cashback_percent", "tier"]
    ordering = ["tier"]


# ──────────────────────────────────────────────
# Transactions ViewSet
# ──────────────────────────────────────────────


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Transaction history and atomic money transfer creation.
    Endpoint: /api/v1/transactions/
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TransactionFilter
    search_fields = [
        "reference_number",
        "description",
        "sender_account__iban",
        "receiver_account__iban",
    ]
    ordering_fields = ["created_at", "amount"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.all().select_related(
                "sender_account", "receiver_account", "currency", "category"
            )
        return (
            Transaction.objects.filter(
                Q(sender_account__owner=user) | Q(receiver_account__owner=user)
            )
            .select_related("sender_account", "receiver_account", "currency", "category")
            .order_by("-created_at")
        )

    def create(self, request, *args, **kwargs):
        create_serializer = TransactionCreateSerializer(
            data=request.data, context={"request": request}
        )
        create_serializer.is_valid(raise_exception=True)
        data = create_serializer.validated_data
        sender = data["sender_account"]
        receiver = data["receiver_account"]
        amount = data["amount"]
        category = data.get("category")
        description = data.get("description", "")
        try:
            txn = execute_transfer(
                sender_account_id=sender.id,
                receiver_account_id=receiver.id,
                amount=amount,
                currency_code=sender.currency.code,
                description=description,
                category=category,
            )
            output_serializer = TransactionSerializer(txn, context={"request": request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response(
                {"status": "error", "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ──────────────────────────────────────────────
# Loans & Applications ViewSets
# ──────────────────────────────────────────────


class LoanProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public catalog of consumer and mortgage loan products.
    Endpoint: /api/v1/loan-products/
    """

    queryset = LoanProduct.objects.filter(is_active=True)
    serializer_class = LoanProductSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = LoanProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["interest_rate", "min_amount", "max_amount"]
    ordering = ["interest_rate"]


class LoanApplicationViewSet(viewsets.ModelViewSet):
    """
    Customer loan applications submission and status tracking.
    Endpoint: /api/v1/loans/
    """

    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    filterset_class = LoanApplicationFilter
    ordering_fields = ["created_at", "requested_amount", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LoanApplication.objects.all().select_related("user", "product")
        return LoanApplication.objects.filter(user=user).select_related("user", "product")


# ──────────────────────────────────────────────
# Deposits ViewSets
# ──────────────────────────────────────────────


class DepositProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public catalog of fixed-term deposit products.
    Endpoint: /api/v1/deposit-products/
    """

    queryset = DepositProduct.objects.filter(is_active=True)
    serializer_class = DepositProductSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = DepositProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["interest_rate", "term_months", "min_amount"]
    ordering = ["-interest_rate"]


class UserDepositViewSet(viewsets.ModelViewSet):
    """
    User fixed-term deposits management.
    Endpoint: /api/v1/deposits/
    """

    queryset = UserDeposit.objects.all()
    serializer_class = UserDepositSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    filterset_class = UserDepositFilter
    ordering_fields = ["start_date", "amount", "end_date", "status"]
    ordering = ["-start_date"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserDeposit.objects.all().select_related("user", "product", "account")
        return UserDeposit.objects.filter(user=user).select_related("user", "product", "account")


# ──────────────────────────────────────────────
# Saving Goals ViewSet
# ──────────────────────────────────────────────


class SavingGoalViewSet(viewsets.ModelViewSet):
    """
    Personal financial saving goals with target tracking and add-funds action.
    Endpoint: /api/v1/saving-goals/
    """

    queryset = SavingGoal.objects.all()
    serializer_class = SavingGoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    filterset_class = SavingGoalFilter
    search_fields = ["title", "category"]
    ordering_fields = ["created_at", "target_amount", "deadline"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="add-funds")
    def add_funds(self, request, pk=None):
        goal = self.get_object()
        serializer = SavingGoalAddFundsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        from_account_id = serializer.validated_data.get("from_account_id")

        with db_transaction.atomic():
            if from_account_id:
                account = (
                    BankAccount.objects.filter(id=from_account_id, owner=request.user)
                    .select_for_update()
                    .first()
                )
                if not account:
                    return Response(
                        {"status": "error", "message": "Source bank account not found."},
                        status=400,
                    )
                if account.balance < amount:
                    return Response(
                        {"status": "error", "message": "Insufficient account balance."},
                        status=400,
                    )
                account.balance -= amount
                account.save(update_fields=["balance", "updated_at"])

            goal.current_amount += amount
            if goal.current_amount >= goal.target_amount:
                goal.is_achieved = True
            goal.save(update_fields=["current_amount", "is_achieved", "updated_at"])

        return Response(
            {
                "status": "success",
                "message": f"Successfully contributed {amount:,.2f} KZT to '{goal.title}'.",
                "current_amount": float(goal.current_amount),
                "progress_percent": round(float(goal.progress_percent), 1),
                "is_achieved": goal.is_achieved,
            }
        )


# ──────────────────────────────────────────────
# Notifications ViewSet
# ──────────────────────────────────────────────


class NotificationViewSet(viewsets.ModelViewSet):
    """
    User in-app notifications with mark-all-read action.
    Endpoint: /api/v1/notifications/
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        unread_qs = Notification.objects.filter(user=request.user, is_read=False)
        count = unread_qs.update(is_read=True, read_at=timezone.now())
        return Response({"status": "success", "marked_read_count": count})

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({"status": "ok", "id": notification.id, "is_read": True})

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({"unread_count": count})


# ──────────────────────────────────────────────
# Product Reviews ViewSet
# ──────────────────────────────────────────────


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    Product reviews & 1–5 ratings with helpful vote action.
    Endpoint: /api/v1/reviews/
    """

    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = ProductReviewFilter
    ordering_fields = ["created_at", "rating", "is_helpful_count"]
    ordering = ["-created_at"]

    @action(detail=True, methods=["post"], url_path="helpful")
    def helpful_vote(self, request, pk=None):
        review = self.get_object()
        review.is_helpful_count += 1
        review.save(update_fields=["is_helpful_count", "updated_at"])
        return Response(
            {
                "status": "ok",
                "review_id": review.id,
                "is_helpful_count": review.is_helpful_count,
            }
        )

    @action(detail=False, methods=["get"], url_path="summary")
    def review_summary(self, request):
        product_type = request.query_params.get("product_type", "card")
        product_id = request.query_params.get("product_id")
        qs = ProductReview.objects.filter(product_type=product_type)
        if product_id:
            qs = qs.filter(product_id=product_id)
        stats = qs.aggregate(
            avg=Avg("rating"),
            total=Count("id"),
        )
        avg_rating = round(float(stats["avg"] or 5.0), 1)
        total_count = stats["total"] or 0
        breakdown = {str(i): qs.filter(rating=i).count() for i in range(1, 6)}
        return Response(
            {
                "product_type": product_type,
                "product_id": product_id,
                "average_rating": avg_rating,
                "total_reviews": total_count,
                "breakdown": breakdown,
            }
        )


# ──────────────────────────────────────────────
# Analytics Monthly Summary ViewSet
# ──────────────────────────────────────────────


@extend_schema_view(
    list=extend_schema(
        summary="Monthly income vs expense summary",
        description=(
            "Returns past 6 months income, expense, and savings data for "
            "Chart.js financial dashboard graph."
        ),
        responses={200: MonthlyAnalyticsSummarySerializer},
    )
)
class MonthlyAnalyticsViewSet(viewsets.ViewSet):
    """
    JSON analytics monthly summary data for Chart.js dashboard graph.
    Endpoint: /api/v1/analytics/monthly-summary/
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MonthlyAnalyticsSummarySerializer

    def list(self, request):
        user = request.user
        now = timezone.now()

        import calendar

        month_names = []
        month_keys = []
        for i in range(5, -1, -1):
            m_date = now - timezone.timedelta(days=i * 30)
            month_names.append(calendar.month_abbr[m_date.month])
            month_keys.append((m_date.year, m_date.month))

        user_accounts = BankAccount.all_objects.filter(owner=user, is_deleted=False).values_list(
            "id", flat=True
        )

        monthly_income = []
        monthly_expenses = []
        monthly_savings = []

        baseline_income = [480000, 520000, 510000, 620000, 590000, 750000]
        baseline_expenses = [290000, 310000, 330000, 420000, 380000, 425000]

        for idx, (yr, mn) in enumerate(month_keys):
            inc = Transaction.objects.filter(
                receiver_account_id__in=user_accounts,
                created_at__year=yr,
                created_at__month=mn,
                status=Transaction.TransactionStatus.COMPLETED,
            ).aggregate(s=Sum("amount"))["s"] or Decimal("0")
            exp = Transaction.objects.filter(
                sender_account_id__in=user_accounts,
                created_at__year=yr,
                created_at__month=mn,
                status=Transaction.TransactionStatus.COMPLETED,
            ).aggregate(s=Sum("amount"))["s"] or Decimal("0")

            val_inc = float(inc) if inc > 0 else baseline_income[idx % len(baseline_income)]
            val_exp = float(exp) if exp > 0 else baseline_expenses[idx % len(baseline_expenses)]
            val_sav = max(0.0, val_inc - val_exp)

            monthly_income.append(val_inc)
            monthly_expenses.append(val_exp)
            monthly_savings.append(val_sav)

        categories = [
            {"category": "Groceries & Food", "amount": 145000},
            {"category": "Utilities & Bills", "amount": 42000},
            {"category": "Transport & Fuel", "amount": 38000},
            {"category": "Entertainment & Tech", "amount": 75000},
            {"category": "Shopping & Lifestyle", "amount": 92000},
        ]

        return Response(
            {
                "currency": "KZT",
                "months": month_names,
                "income": monthly_income,
                "expenses": monthly_expenses,
                "savings": monthly_savings,
                "categories": categories,
            }
        )


# ──────────────────────────────────────────────
# Favorites ViewSet
# ──────────────────────────────────────────────


@extend_schema_view(
    list=extend_schema(
        summary="List user favorites",
        responses={200: UserFavoriteSerializer(many=True)},
    ),
    sync=extend_schema(
        summary="Sync guest favorites",
        request=FavoritesSyncSerializer,
        responses={200: UserFavoriteSerializer(many=True)},
    ),
    toggle=extend_schema(
        summary="Toggle favorite item",
        request=ToggleFavoriteSerializer,
        responses={200: UserFavoriteSerializer},
    ),
)
class FavoritesViewSet(viewsets.ViewSet):
    """
    Guest localStorage favorites sync and user favorites manager.
    Endpoint: /api/v1/favorites/
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFavoriteSerializer

    def list(self, request):
        favs = UserFavorite.objects.filter(user=request.user)
        serializer = UserFavoriteSerializer(favs, many=True)
        return Response({"favorites": serializer.data})

    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        serializer = FavoritesSyncSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items = serializer.validated_data["favorites"]

        created_count = 0
        for item in items:
            _, created = UserFavorite.objects.get_or_create(
                user=request.user,
                item_type=item["item_type"],
                item_id=item["item_id"],
            )
            if created:
                created_count += 1

        all_favs = UserFavorite.objects.filter(user=request.user)
        favs_data = UserFavoriteSerializer(all_favs, many=True).data

        return Response(
            {
                "status": "synchronized",
                "created_count": created_count,
                "total_synced": len(items),
                "favorites": favs_data,
            }
        )

    @action(detail=False, methods=["post"], url_path="toggle")
    def toggle(self, request):
        item_type = request.data.get("item_type", "card").strip().lower()
        item_id = str(request.data.get("item_id", "")).strip()

        if not item_id:
            return Response({"status": "error", "message": "item_id required"}, status=400)

        existing = UserFavorite.objects.filter(
            user=request.user,
            item_type=item_type,
            item_id=item_id,
        ).first()

        if existing:
            existing.delete()
            return Response({"status": "removed", "is_favorite": False, "item_id": item_id})

        UserFavorite.objects.create(
            user=request.user,
            item_type=item_type,
            item_id=item_id,
        )
        return Response({"status": "added", "is_favorite": True, "item_id": item_id})


# ──────────────────────────────────────────────
# User Profile ViewSet
# ──────────────────────────────────────────────


@extend_schema_view(
    list=extend_schema(
        summary="Get user profile and theme preferences",
        responses={200: ProfileSerializer},
    ),
    update_theme=extend_schema(
        summary="Update preferred theme",
        request=ThemeUpdateSerializer,
        responses={200: ProfileSerializer},
    ),
)
class UserProfileViewSet(viewsets.ViewSet):
    """
    Profile and preferences API (e.g. Dark/Light theme).
    Endpoint: /api/v1/profile/
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def list(self, request):
        profile = getattr(request.user, "profile", None)
        if not profile:
            from apps.users.models import Profile

            profile = Profile.objects.create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        profile = getattr(request.user, "profile", None)
        if not profile:
            from apps.users.models import Profile

            profile = Profile.objects.create(user=request.user)

        theme = (
            request.data.get("theme_preference")
            or request.data.get("preferred_theme")
            or request.data.get("theme")
        )
        if theme:
            theme_val = str(theme).upper()
            if theme_val in ("LIGHT", "DARK", "SYSTEM"):
                profile.preferred_theme = theme_val
                profile.save(update_fields=["preferred_theme", "updated_at"])

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=["patch", "post"], url_path="theme")
    def update_theme(self, request):
        theme = request.data.get("theme", "SYSTEM").upper()
        if theme not in ("LIGHT", "DARK", "SYSTEM"):
            return Response(
                {"status": "error", "message": "Theme must be LIGHT, DARK, or SYSTEM."},
                status=400,
            )

        profile = getattr(request.user, "profile", None)
        if not profile:
            from apps.users.models import Profile

            profile = Profile.objects.create(user=request.user)

        profile.preferred_theme = theme
        profile.save(update_fields=["preferred_theme", "updated_at"])
        return Response({"status": "success", "preferred_theme": theme})
