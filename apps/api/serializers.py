"""
DRF Serializers for RocketBank REST API.
Demonstrates:
- Nested serializers
- SerializerMethodField
- Custom field-level validators (`validate_<field>`)
- Object-level validation (`validate()`)
"""

from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from apps.accounts.models import BankAccount, Currency
from apps.analytics.models import SavingGoal
from apps.cards.models import BankCard, CardProduct
from apps.credits.models import LoanApplication, LoanProduct
from apps.deposits.models import DepositProduct, UserDeposit
from apps.notifications.models import Notification
from apps.support.models import ProductReview
from apps.transactions.models import Transaction, TransactionCategory
from apps.users.models import Profile, User, UserFavorite

# ──────────────────────────────────────────────
# Users & Profiles
# ──────────────────────────────────────────────


class UserSummarySerializer(serializers.ModelSerializer):
    """Compact user representation for nested embedding."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "is_verified",
        ]
        read_only_fields = fields


class ProfileSerializer(serializers.ModelSerializer):
    """User profile serializer with nested user and theme preference."""

    user = UserSummarySerializer(read_only=True)
    theme_preference = serializers.CharField(source="preferred_theme", required=False)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "avatar",
            "birth_date",
            "address",
            "kyc_status",
            "preferred_theme",
            "theme_preference",
            "preferred_language",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "kyc_status", "created_at", "updated_at"]

    def validate_preferred_theme(self, value):
        valid_themes = [c[0] for c in Profile.ThemeChoice.choices]
        if value.upper() not in valid_themes:
            raise serializers.ValidationError(f"Invalid theme '{value}'. Choices: {valid_themes}")
        return value.upper()

    def validate_theme_preference(self, value):
        return self.validate_preferred_theme(value)


# ──────────────────────────────────────────────
# Accounts & Currency
# ──────────────────────────────────────────────


class CurrencySerializer(serializers.ModelSerializer):
    """Supported currency serializer."""

    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol", "exchange_rate_to_kzt", "is_active"]


class BankAccountSerializer(serializers.ModelSerializer):
    """Bank account serializer with nested currency and SerializerMethodField."""

    currency = CurrencySerializer(read_only=True)
    currency_code = serializers.CharField(write_only=True, required=False, default="KZT")
    owner = UserSummarySerializer(read_only=True)
    status_display = serializers.SerializerMethodField()
    account_type_display = serializers.SerializerMethodField()
    formatted_balance = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = [
            "id",
            "iban",
            "account_type",
            "account_type_display",
            "currency",
            "currency_code",
            "balance",
            "formatted_balance",
            "status",
            "status_display",
            "owner",
            "opened_at",
            "created_at",
        ]
        read_only_fields = ["id", "balance", "formatted_balance", "opened_at", "created_at"]

    def get_status_display(self, obj) -> str:
        return obj.get_status_display()

    def get_account_type_display(self, obj) -> str:
        return obj.get_account_type_display()

    def get_formatted_balance(self, obj) -> str:
        symbol = obj.currency.symbol if obj.currency else ""
        return f"{obj.balance:,.2f} {symbol}".strip()

    def validate_iban(self, value):
        from apps.core.validators import validate_iban as validate_iban_func

        try:
            validate_iban_func(value)
        except Exception as exc:
            raise serializers.ValidationError(str(exc))
        return value.upper().replace(" ", "")

    def validate(self, attrs):
        user = self.context["request"].user
        account_type = attrs.get("account_type", BankAccount.AccountType.CHECKING)
        currency_code = attrs.get("currency_code", "KZT")

        currency = Currency.objects.filter(code=currency_code, is_active=True).first()
        if not currency:
            raise serializers.ValidationError(
                {"currency_code": f"Currency '{currency_code}' not supported or inactive."}
            )
        attrs["currency"] = currency

        # On create, ensure unique per (owner, currency, account_type)
        if not self.instance:
            exists = BankAccount.all_objects.filter(
                owner=user,
                currency=currency,
                account_type=account_type,
                is_deleted=False,
            ).exists()
            if exists:
                raise serializers.ValidationError(
                    f"You already have an active {account_type} account in {currency_code}."
                )
        return attrs

    def create(self, validated_data):
        import uuid

        validated_data.pop("currency_code", None)
        user = self.context["request"].user
        validated_data["owner"] = user

        if "iban" not in validated_data or not validated_data["iban"]:
            # Auto-generate a valid KZ IBAN
            random_digits = "".join([str(uuid.uuid4().int % 10) for _ in range(16)])
            validated_data["iban"] = f"KZ{uuid.uuid4().int % 90 + 10}ROCK{random_digits}"[:20]

        return super().create(validated_data)


# ──────────────────────────────────────────────
# Cards & Card Products
# ──────────────────────────────────────────────


class CardProductSerializer(serializers.ModelSerializer):
    """Catalog of credit/debit card products."""

    tier_display = serializers.SerializerMethodField()

    class Meta:
        model = CardProduct
        fields = [
            "id",
            "slug",
            "title",
            "tier",
            "tier_display",
            "cashback_percent",
            "annual_fee",
            "description",
            "is_active",
            "created_at",
        ]

    def get_tier_display(self, obj) -> str:
        return obj.get_tier_display()


class BankCardSerializer(serializers.ModelSerializer):
    """Issued card details with nested CardProduct and state information."""

    product = CardProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=CardProduct.objects.filter(is_active=True),
        source="product",
        write_only=True,
    )
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all(),
        source="account",
        write_only=True,
    )
    account_iban = serializers.CharField(source="account.iban", read_only=True)
    status_display = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = BankCard
        fields = [
            "id",
            "account_id",
            "account_iban",
            "product",
            "product_id",
            "card_number_masked",
            "expiry_date",
            "status",
            "status_display",
            "daily_limit",
            "is_expired",
            "issued_at",
        ]
        read_only_fields = ["id", "card_number_masked", "issued_at"]

    def get_status_display(self, obj) -> str:
        return obj.get_status_display()

    def get_is_expired(self, obj) -> bool:
        return obj.expiry_date < timezone.now().date()

    def validate_daily_limit(self, value):
        if value < 0:
            raise serializers.ValidationError("Daily limit cannot be negative.")
        if value > Decimal("50000000"):
            raise serializers.ValidationError("Daily limit exceeds system maximum (50,000,000).")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        account = attrs.get("account")
        if account and account.owner != user:
            raise serializers.ValidationError(
                {"account_id": "You can only issue cards for your own accounts."}
            )
        return attrs


class BankCardLimitUpdateSerializer(serializers.Serializer):
    """Serializer for updating card daily limit."""

    daily_limit = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.00")
    )

    def validate_daily_limit(self, value):
        if value < 0:
            raise serializers.ValidationError("Daily limit cannot be negative.")
        if value > Decimal("50000000"):
            raise serializers.ValidationError("Daily limit exceeds maximum permitted limit.")
        return value


# ──────────────────────────────────────────────
# Transactions
# ──────────────────────────────────────────────


class TransactionCategorySerializer(serializers.ModelSerializer):
    """Category serializer for transactions."""

    class Meta:
        model = TransactionCategory
        fields = ["id", "name", "slug", "icon", "is_expense"]


class TransactionSerializer(serializers.ModelSerializer):
    """Comprehensive transaction representation with nested currency & category."""

    currency = CurrencySerializer(read_only=True)
    category = TransactionCategorySerializer(read_only=True)
    sender_iban = serializers.CharField(source="sender_account.iban", default=None, read_only=True)
    receiver_iban = serializers.CharField(
        source="receiver_account.iban", default=None, read_only=True
    )
    status_display = serializers.SerializerMethodField()
    transaction_type_display = serializers.SerializerMethodField()
    is_outflow = serializers.SerializerMethodField()
    formatted_amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "reference_number",
            "sender_account",
            "sender_iban",
            "receiver_account",
            "receiver_iban",
            "category",
            "amount",
            "formatted_amount",
            "currency",
            "status",
            "status_display",
            "transaction_type",
            "transaction_type_display",
            "description",
            "is_outflow",
            "created_at",
        ]
        read_only_fields = fields

    def get_status_display(self, obj) -> str:
        return obj.get_status_display()

    def get_transaction_type_display(self, obj) -> str:
        return obj.get_transaction_type_display()

    def get_is_outflow(self, obj) -> bool:
        user = self.context.get("request", None) and self.context["request"].user
        if not user or not user.is_authenticated:
            return False
        return bool(obj.sender_account and obj.sender_account.owner_id == user.id)

    def get_formatted_amount(self, obj) -> str:
        prefix = "-" if self.get_is_outflow(obj) else "+"
        return f"{prefix}{obj.amount:,.2f} {obj.currency.code}"


class TransactionCreateSerializer(serializers.Serializer):
    """Atomic transfer creation serializer."""

    sender_account_id = serializers.UUIDField(required=True)
    receiver_iban = serializers.CharField(max_length=34, required=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal("0.01"))
    category_id = serializers.IntegerField(required=False, allow_null=True)
    description = serializers.CharField(
        max_length=255, required=False, allow_blank=True, default=""
    )

    def validate_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Transfer amount must be strictly greater than 0.")
        if value.as_tuple().exponent < -2:
            raise serializers.ValidationError("Amount cannot have more than 2 decimal places.")
        return value

    def validate_receiver_iban(self, value):
        from apps.core.validators import validate_iban as validate_iban_func

        clean = value.upper().replace(" ", "")
        try:
            validate_iban_func(clean)
        except Exception as exc:
            raise serializers.ValidationError(str(exc))
        return clean

    def validate(self, attrs):
        user = self.context["request"].user
        sender_id = attrs["sender_account_id"]
        receiver_iban = attrs["receiver_iban"]
        amount = attrs["amount"]

        sender = (
            BankAccount.all_objects.filter(id=sender_id, is_deleted=False)
            .select_related("currency")
            .first()
        )
        if not sender:
            raise serializers.ValidationError({"sender_account_id": "Sender account not found."})

        if sender.owner != user and not user.is_staff:
            raise serializers.ValidationError(
                {"sender_account_id": "You can only transfer from accounts you own."}
            )

        if sender.status != BankAccount.AccountStatus.ACTIVE:
            raise serializers.ValidationError(
                {"sender_account_id": f"Sender account is {sender.get_status_display()}."}
            )

        if sender.balance < amount:
            raise serializers.ValidationError(
                {"amount": f"Insufficient funds. Balance: {sender.balance:,.2f}"}
            )

        receiver = BankAccount.all_objects.filter(iban=receiver_iban, is_deleted=False).first()
        if not receiver:
            raise serializers.ValidationError(
                {"receiver_iban": f"No account found with IBAN {receiver_iban}."}
            )

        if str(sender.id) == str(receiver.id):
            raise serializers.ValidationError(
                {"receiver_iban": "Cannot transfer to the exact same account."}
            )

        if receiver.status != BankAccount.AccountStatus.ACTIVE:
            raise serializers.ValidationError(
                {"receiver_iban": "Recipient account is currently unable to accept transfers."}
            )

        attrs["sender_account"] = sender
        attrs["receiver_account"] = receiver

        cat_id = attrs.get("category_id")
        if cat_id:
            cat = TransactionCategory.objects.filter(id=cat_id).first()
            attrs["category"] = cat
        else:
            attrs["category"] = None

        return attrs


# ──────────────────────────────────────────────
# Loans & Loan Products
# ──────────────────────────────────────────────


class LoanProductSerializer(serializers.ModelSerializer):
    """Loan product catalog serializer."""

    class Meta:
        model = LoanProduct
        fields = [
            "id",
            "slug",
            "title",
            "min_amount",
            "max_amount",
            "interest_rate",
            "min_term_months",
            "max_term_months",
            "description",
            "is_active",
            "created_at",
        ]


class LoanApplicationSerializer(serializers.ModelSerializer):
    """Customer loan application serializer with validation."""

    product = LoanProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=LoanProduct.objects.filter(is_active=True),
        source="product",
        write_only=True,
    )
    user = UserSummarySerializer(read_only=True)
    status_display = serializers.SerializerMethodField()
    estimated_monthly_payment = serializers.SerializerMethodField()

    class Meta:
        model = LoanApplication
        fields = [
            "id",
            "user",
            "product",
            "product_id",
            "requested_amount",
            "term_months",
            "monthly_income",
            "status",
            "status_display",
            "estimated_monthly_payment",
            "approved_at",
            "rejection_reason",
            "created_at",
        ]
        read_only_fields = ["id", "user", "status", "approved_at", "rejection_reason", "created_at"]

    def get_status_display(self, obj) -> str:
        return obj.get_status_display()

    def get_estimated_monthly_payment(self, obj) -> float:
        # Standard Annuity formula: P * r * (1+r)^n / ((1+r)^n - 1)
        try:
            P = float(obj.requested_amount)
            annual_rate = float(obj.product.interest_rate) / 100.0
            r = annual_rate / 12.0
            n = obj.term_months
            if r == 0:
                return round(P / n, 2)
            payment = P * (r * ((1 + r) ** n)) / (((1 + r) ** n) - 1)
            return round(payment, 2)
        except Exception:
            return 0.0

    def validate_requested_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Requested loan amount must be positive.")
        return value

    def validate_term_months(self, value):
        if value <= 0:
            raise serializers.ValidationError("Term months must be positive.")
        return value

    def validate(self, attrs):
        product = attrs.get("product")
        amount = attrs.get("requested_amount")
        term = attrs.get("term_months")

        if product and amount:
            if not (product.min_amount <= amount <= product.max_amount):
                msg = f"Must be between {product.min_amount:,.2f} and {product.max_amount:,.2f}."
                raise serializers.ValidationError({"requested_amount": msg})
        if product and term:
            if not (product.min_term_months <= term <= product.max_term_months):
                msg = (
                    f"Must be between {product.min_term_months} and "
                    f"{product.max_term_months} months."
                )
                raise serializers.ValidationError({"term_months": msg})
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        validated_data["status"] = LoanApplication.LoanStatus.SUBMITTED
        return super().create(validated_data)


# ──────────────────────────────────────────────
# Deposits & Deposit Products
# ──────────────────────────────────────────────


class DepositProductSerializer(serializers.ModelSerializer):
    """Deposit product catalog serializer."""

    class Meta:
        model = DepositProduct
        fields = [
            "id",
            "slug",
            "title",
            "interest_rate",
            "min_amount",
            "term_months",
            "is_early_withdrawal_allowed",
            "description",
            "is_active",
            "created_at",
        ]


class UserDepositSerializer(serializers.ModelSerializer):
    """User fixed deposit serializer."""

    product = DepositProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=DepositProduct.objects.filter(is_active=True),
        source="product",
        write_only=True,
    )
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all(),
        source="account",
        write_only=True,
    )
    account_iban = serializers.CharField(source="account.iban", read_only=True)
    status_display = serializers.SerializerMethodField()
    expected_interest = serializers.SerializerMethodField()

    class Meta:
        model = UserDeposit
        fields = [
            "id",
            "product",
            "product_id",
            "account_id",
            "account_iban",
            "amount",
            "accrued_interest",
            "expected_interest",
            "start_date",
            "end_date",
            "status",
            "status_display",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "accrued_interest",
            "start_date",
            "end_date",
            "status",
            "created_at",
        ]

    def get_status_display(self, obj) -> str:
        return obj.get_status_display()

    def get_expected_interest(self, obj) -> float:
        try:
            P = float(obj.amount)
            r = float(obj.product.interest_rate) / 100.0
            years = obj.product.term_months / 12.0
            return round(P * r * years, 2)
        except Exception:
            return 0.0

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Deposit amount must be positive.")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        account = attrs.get("account")
        product = attrs.get("product")
        amount = attrs.get("amount")

        if account and account.owner != user:
            raise serializers.ValidationError(
                {"account_id": "You can only fund deposits from your own accounts."}
            )

        if account and amount and account.balance < amount:
            raise serializers.ValidationError(
                {"amount": f"Insufficient funds on account {account.iban}."}
            )

        if product and amount and amount < product.min_amount:
            raise serializers.ValidationError(
                {"amount": f"Minimum deposit for {product.title} is {product.min_amount:,.2f}."}
            )

        return attrs

    def create(self, validated_data):
        from dateutil.relativedelta import relativedelta

        user = self.context["request"].user
        account = validated_data["account"]
        product = validated_data["product"]
        amount = validated_data["amount"]

        # Deduct from funding account
        account.balance -= amount
        account.save(update_fields=["balance", "updated_at"])

        start_date = timezone.now().date()
        end_date = start_date + relativedelta(months=product.term_months)

        validated_data["user"] = user
        validated_data["start_date"] = start_date
        validated_data["end_date"] = end_date
        validated_data["status"] = UserDeposit.DepositStatus.ACTIVE

        return super().create(validated_data)


# ──────────────────────────────────────────────
# Saving Goals
# ──────────────────────────────────────────────


class SavingGoalSerializer(serializers.ModelSerializer):
    """User saving goal serializer."""

    progress_percent = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()

    class Meta:
        model = SavingGoal
        fields = [
            "id",
            "title",
            "target_amount",
            "current_amount",
            "progress_percent",
            "remaining_amount",
            "deadline",
            "category",
            "is_achieved",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "progress_percent",
            "remaining_amount",
            "created_at",
            "updated_at",
        ]

    def get_progress_percent(self, obj) -> float:
        return round(float(obj.progress_percent), 1)

    def get_remaining_amount(self, obj) -> float:
        remaining = max(Decimal("0.00"), obj.target_amount - obj.current_amount)
        return float(remaining)

    def validate_target_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Target amount must be strictly greater than 0.")
        return value

    def validate_current_amount(self, value):
        if value < Decimal("0.00"):
            raise serializers.ValidationError("Current amount cannot be negative.")
        return value

    def validate(self, attrs):
        target = attrs.get("target_amount", getattr(self.instance, "target_amount", None))
        current = attrs.get("current_amount", getattr(self.instance, "current_amount", None))
        if target is not None and current is not None:
            attrs["is_achieved"] = current >= target
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class SavingGoalAddFundsSerializer(serializers.Serializer):
    """Serializer to deposit funds into a saving goal."""

    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal("0.01"))
    from_account_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Deposit amount must be positive.")
        return value


# ──────────────────────────────────────────────
# Notifications
# ──────────────────────────────────────────────


class NotificationSerializer(serializers.ModelSerializer):
    """In-app notification serializer."""

    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "notification_type",
            "is_read",
            "read_at",
            "time_ago",
            "created_at",
        ]
        read_only_fields = ["id", "title", "message", "notification_type", "created_at"]

    def get_time_ago(self, obj) -> str:
        delta = timezone.now() - obj.created_at
        if delta.days > 0:
            return f"{delta.days}d ago"
        hours = delta.seconds // 3600
        if hours > 0:
            return f"{hours}h ago"
        minutes = delta.seconds // 60
        return f"{minutes}m ago" if minutes > 0 else "just now"


# ──────────────────────────────────────────────
# Reviews & Ratings
# ──────────────────────────────────────────────


class ProductReviewSerializer(serializers.ModelSerializer):
    """Product review serializer with rating and helpful votes."""

    author_name = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = [
            "id",
            "product_type",
            "product_id",
            "product_title",
            "author_name",
            "rating",
            "comment",
            "is_helpful_count",
            "is_author",
            "created_at",
        ]
        read_only_fields = ["id", "author_name", "is_helpful_count", "is_author", "created_at"]

    def get_author_name(self, obj) -> str:
        if obj.user:
            return obj.user.first_name or obj.user.username.split("@")[0]
        return "Verified Customer"

    def get_is_author(self, obj) -> bool:
        user = self.context.get("request", None) and self.context["request"].user
        return bool(user and user.is_authenticated and obj.user_id == user.id)

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be an integer between 1 and 5.")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication required to submit a review.")
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


# ──────────────────────────────────────────────
# Favorites & Guest Sync
# ──────────────────────────────────────────────


class UserFavoriteSerializer(serializers.ModelSerializer):
    """User favorite item serializer."""

    class Meta:
        model = UserFavorite
        fields = ["id", "item_type", "item_id", "created_at"]
        read_only_fields = ["id", "created_at"]


class FavoritesSyncSerializer(serializers.Serializer):
    """Sync guest favorites from localStorage to authenticated user."""

    favorites = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=True,
        help_text="Array of objects: [{'item_type': 'card', 'item_id': 'platinum-card'}, ...]",
    )

    def validate_favorites(self, value):
        cleaned = []
        for item in value:
            item_type = item.get("item_type") or item.get("product_type", "card")
            item_id = item.get("item_id") or item.get("product_id")
            if item_id:
                cleaned.append(
                    {
                        "item_type": str(item_type).strip().lower(),
                        "item_id": str(item_id).strip(),
                    }
                )
        return cleaned


class ToggleFavoriteSerializer(serializers.Serializer):
    """Toggle favorite status for an item."""

    item_type = serializers.CharField(default="card")
    item_id = serializers.CharField()


class MonthlyCategoryExpenseSerializer(serializers.Serializer):
    """Category expense breakdown serializer."""

    category = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class MonthlyAnalyticsSummarySerializer(serializers.Serializer):
    """Monthly financial summary serializer for Chart.js graph."""

    currency = serializers.CharField()
    months = serializers.ListField(child=serializers.CharField())
    income = serializers.ListField(child=serializers.FloatField())
    expenses = serializers.ListField(child=serializers.FloatField())
    savings = serializers.ListField(child=serializers.FloatField())
    categories = MonthlyCategoryExpenseSerializer(many=True)


class ThemeUpdateSerializer(serializers.Serializer):
    """Theme update request serializer."""

    theme = serializers.ChoiceField(choices=["LIGHT", "DARK", "SYSTEM"])
