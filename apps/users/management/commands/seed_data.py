"""
Management command to seed the database with sample data.

Creates role groups, test users, reference data (currencies,
card products, loan products, deposit products, categories, FAQs),
and at least 500 records across all domain models.

Usage:
    python manage.py seed_data
    python manage.py seed_data --flush  # Clear existing data first
"""

import random
import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from apps.accounts.models import (
    BankAccount,
    Beneficiary,
    Currency,
    SavedBeneficiary,
)
from apps.analytics.models import SavingGoal
from apps.cards.models import BankCard, CardProduct
from apps.credits.models import LoanApplication, LoanProduct, LoanSchedule
from apps.deposits.models import DepositProduct, UserDeposit
from apps.notifications.models import Notification
from apps.support.models import FAQ, SupportTicket, TicketReview
from apps.transactions.models import Transaction, TransactionCategory
from apps.users.models import User

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample data (500+ records)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing seeded data before creating new.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing data...")
            self._flush()

        self.stdout.write("Seeding database...")

        groups = self._create_groups()
        users = self._create_users(groups)
        currencies = self._create_currencies()
        categories = self._create_transaction_categories()
        card_products = self._create_card_products()
        loan_products = self._create_loan_products()
        deposit_products = self._create_deposit_products()
        self._create_faqs()

        accounts = self._create_bank_accounts(
            users, currencies
        )
        cards = self._create_bank_cards(accounts, card_products)
        transactions = self._create_transactions(
            accounts, currencies, categories
        )
        loans = self._create_loans(users, loan_products)
        deposits = self._create_deposits(
            users, accounts, deposit_products
        )
        self._create_saving_goals(users)
        self._create_notifications(users)
        self._create_support_tickets(users)
        self._create_beneficiaries(users, accounts)

        total = self._count_records()
        self.stdout.write(
            self.style.SUCCESS(
                f"Database seeded successfully! "
                f"Total records: {total}"
            )
        )

    def _flush(self):
        """Delete all seeded data."""
        TicketReview.objects.all().delete()
        SupportTicket.objects.all().delete()
        FAQ.objects.all().delete()
        Notification.objects.all().delete()
        SavingGoal.objects.all().delete()
        UserDeposit.objects.all().delete()
        LoanSchedule.objects.all().delete()
        LoanApplication.objects.all().delete()
        Transaction.objects.all().delete()
        BankCard.objects.all().delete()
        SavedBeneficiary.objects.all().delete()
        Beneficiary.objects.all().delete()
        BankAccount.all_objects.all().delete()
        DepositProduct.objects.all().delete()
        LoanProduct.objects.all().delete()
        CardProduct.objects.all().delete()
        TransactionCategory.objects.all().delete()
        Currency.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        Group.objects.all().delete()

    def _count_records(self) -> int:
        """Count total records across all domain models."""
        return sum([
            User.objects.count(),
            BankAccount.all_objects.count(),
            BankCard.objects.count(),
            Transaction.objects.count(),
            LoanApplication.objects.count(),
            LoanSchedule.objects.count(),
            UserDeposit.objects.count(),
            Notification.objects.count(),
            SavingGoal.objects.count(),
            SupportTicket.objects.count(),
            TicketReview.objects.count(),
            FAQ.objects.count(),
            Beneficiary.objects.count(),
            SavedBeneficiary.objects.count(),
            Currency.objects.count(),
            CardProduct.objects.count(),
            LoanProduct.objects.count(),
            DepositProduct.objects.count(),
            TransactionCategory.objects.count(),
        ])

    def _create_groups(self) -> dict:
        """Create Client, Manager, and Admin groups."""
        groups = {}
        group_perms = {
            "Client": [
                "view_bankaccount",
                "view_bankcard",
                "view_transaction",
                "view_notification",
                "add_supportticket",
                "view_supportticket",
            ],
            "Manager": [
                "view_bankaccount",
                "change_bankaccount",
                "view_bankcard",
                "change_bankcard",
                "view_transaction",
                "change_transaction",
                "view_loanapplication",
                "change_loanapplication",
                "view_supportticket",
                "change_supportticket",
                "view_notification",
                "add_notification",
            ],
            "Admin": [],  # gets all permissions
        }

        for name, perm_codenames in group_perms.items():
            group, _ = Group.objects.get_or_create(name=name)
            if perm_codenames:
                perms = Permission.objects.filter(
                    codename__in=perm_codenames
                )
                group.permissions.set(perms)
            elif name == "Admin":
                group.permissions.set(
                    Permission.objects.all()
                )
            groups[name] = group
            self.stdout.write(f"  Created group: {name}")

        return groups

    def _create_users(self, groups: dict) -> list:
        """Create 3 default test users + additional random users."""
        users = []

        # Default test users
        test_users_data = [
            {
                "email": "client@rocketbank.company",
                "username": "client",
                "first_name": "Client",
                "last_name": "User",
                "group": "Client",
                "is_staff": False,
            },
            {
                "email": "manager@rocketbank.company",
                "username": "manager",
                "first_name": "Manager",
                "last_name": "User",
                "group": "Manager",
                "is_staff": True,
            },
            {
                "email": "admin@rocketbank.company",
                "username": "admin_user",
                "first_name": "Admin",
                "last_name": "User",
                "group": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
        ]

        for data in test_users_data:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "username": data["username"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_staff": data.get("is_staff", False),
                    "is_superuser": data.get(
                        "is_superuser", False
                    ),
                    "is_verified": True,
                    "phone_number": fake.phone_number()[:20],
                },
            )
            if created:
                user.set_password("RocketBank2024!")
                user.save()
                user.groups.add(groups[data["group"]])
            users.append(user)
            self.stdout.write(f"  User: {data['email']}")

        # Additional random users
        for i in range(17):
            email = f"user{i+1}@rocketbank.company"
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": f"user{i+1}",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "phone_number": fake.phone_number()[:20],
                    "is_verified": random.choice(
                        [True, True, False]
                    ),
                },
            )
            if created:
                user.set_password("RocketBank2024!")
                user.save()
                user.groups.add(groups["Client"])
            users.append(user)

        self.stdout.write(
            f"  Created {len(users)} users total"
        )
        return users

    def _create_currencies(self) -> list:
        """Create default currencies."""
        currencies_data = [
            ("KZT", "Kazakhstani Tenge", "₸", Decimal("1")),
            ("USD", "US Dollar", "$", Decimal("470.50")),
            ("EUR", "Euro", "€", Decimal("512.30")),
            ("RUB", "Russian Ruble", "₽", Decimal("5.12")),
            ("GBP", "British Pound", "£", Decimal("596.80")),
        ]
        currencies = []
        for code, name, symbol, rate in currencies_data:
            curr, _ = Currency.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "symbol": symbol,
                    "exchange_rate_to_kzt": rate,
                },
            )
            currencies.append(curr)

        self.stdout.write(
            f"  Created {len(currencies)} currencies"
        )
        return currencies

    def _create_transaction_categories(self) -> list:
        """Create transaction categories."""
        cats_data = [
            ("Groceries", "groceries", "fa-shopping-cart", True),
            ("Transport", "transport", "fa-bus", True),
            ("Entertainment", "entertainment", "fa-film", True),
            ("Utilities", "utilities", "fa-bolt", True),
            ("Healthcare", "healthcare", "fa-medkit", True),
            ("Education", "education", "fa-book", True),
            ("Salary", "salary", "fa-money-bill", False),
            ("Freelance", "freelance", "fa-laptop", False),
            ("Investment", "investment", "fa-chart-line", False),
            ("Transfer", "transfer", "fa-exchange-alt", True),
            ("Restaurant", "restaurant", "fa-utensils", True),
            ("Shopping", "shopping", "fa-bag-shopping", True),
        ]
        categories = []
        for name, slug, icon, is_expense in cats_data:
            cat, _ = TransactionCategory.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "icon": icon,
                    "is_expense": is_expense,
                },
            )
            categories.append(cat)

        self.stdout.write(
            f"  Created {len(categories)} transaction categories"
        )
        return categories

    def _create_card_products(self) -> list:
        """Create card product catalog."""
        products_data = [
            {
                "slug": "standard-card",
                "title": "RocketBank Standard",
                "tier": CardProduct.CardTier.STANDARD,
                "cashback_percent": Decimal("0.50"),
                "annual_fee": Decimal("0"),
            },
            {
                "slug": "gold-card",
                "title": "RocketBank Gold",
                "tier": CardProduct.CardTier.GOLD,
                "cashback_percent": Decimal("1.00"),
                "annual_fee": Decimal("5000"),
            },
            {
                "slug": "platinum-card",
                "title": "RocketBank Platinum",
                "tier": CardProduct.CardTier.PLATINUM,
                "cashback_percent": Decimal("2.00"),
                "annual_fee": Decimal("15000"),
            },
            {
                "slug": "black-card",
                "title": "RocketBank Black",
                "tier": CardProduct.CardTier.BLACK,
                "cashback_percent": Decimal("5.00"),
                "annual_fee": Decimal("50000"),
            },
        ]
        products = []
        for data in products_data:
            prod, _ = CardProduct.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "tier": data["tier"],
                    "cashback_percent": data["cashback_percent"],
                    "annual_fee": data["annual_fee"],
                    "description": (
                        f"{data['title']} card with "
                        f"{data['cashback_percent']}% cashback."
                    ),
                },
            )
            products.append(prod)

        self.stdout.write(
            f"  Created {len(products)} card products"
        )
        return products

    def _create_loan_products(self) -> list:
        """Create loan product catalog."""
        products_data = [
            {
                "slug": "consumer-loan",
                "title": "Consumer Loan",
                "min_amount": Decimal("50000"),
                "max_amount": Decimal("5000000"),
                "interest_rate": Decimal("18.90"),
                "min_term_months": 3,
                "max_term_months": 60,
            },
            {
                "slug": "mortgage",
                "title": "Mortgage",
                "min_amount": Decimal("5000000"),
                "max_amount": Decimal("100000000"),
                "interest_rate": Decimal("12.50"),
                "min_term_months": 12,
                "max_term_months": 300,
            },
            {
                "slug": "auto-loan",
                "title": "Auto Loan",
                "min_amount": Decimal("500000"),
                "max_amount": Decimal("30000000"),
                "interest_rate": Decimal("15.00"),
                "min_term_months": 6,
                "max_term_months": 84,
            },
            {
                "slug": "business-loan",
                "title": "Business Loan",
                "min_amount": Decimal("1000000"),
                "max_amount": Decimal("50000000"),
                "interest_rate": Decimal("16.50"),
                "min_term_months": 6,
                "max_term_months": 120,
            },
        ]
        products = []
        for data in products_data:
            prod, _ = LoanProduct.objects.get_or_create(
                slug=data["slug"],
                defaults=data,
            )
            products.append(prod)

        self.stdout.write(
            f"  Created {len(products)} loan products"
        )
        return products

    def _create_deposit_products(self) -> list:
        """Create deposit product catalog."""
        products_data = [
            {
                "slug": "standard-deposit",
                "title": "Standard Deposit",
                "interest_rate": Decimal("10.50"),
                "min_amount": Decimal("100000"),
                "term_months": 12,
                "is_early_withdrawal_allowed": False,
            },
            {
                "slug": "flexible-deposit",
                "title": "Flexible Deposit",
                "interest_rate": Decimal("8.00"),
                "min_amount": Decimal("50000"),
                "term_months": 6,
                "is_early_withdrawal_allowed": True,
            },
            {
                "slug": "premium-deposit",
                "title": "Premium Deposit",
                "interest_rate": Decimal("13.00"),
                "min_amount": Decimal("1000000"),
                "term_months": 24,
                "is_early_withdrawal_allowed": False,
            },
        ]
        products = []
        for data in products_data:
            prod, _ = DepositProduct.objects.get_or_create(
                slug=data["slug"],
                defaults=data,
            )
            products.append(prod)

        self.stdout.write(
            f"  Created {len(products)} deposit products"
        )
        return products

    def _create_faqs(self):
        """Create FAQ entries."""
        faqs_data = [
            {
                "question": "How do I open a bank account?",
                "answer": (
                    "You can open an account through our mobile "
                    "app or by visiting any branch."
                ),
                "category": "Accounts",
                "order": 1,
            },
            {
                "question": "What are the card tiers available?",
                "answer": (
                    "We offer Standard, Gold, Platinum, and "
                    "Black card tiers."
                ),
                "category": "Cards",
                "order": 1,
            },
            {
                "question": "How do I apply for a loan?",
                "answer": (
                    "Submit a loan application through the app "
                    "with your income documents."
                ),
                "category": "Loans",
                "order": 1,
            },
            {
                "question": "What is the minimum deposit amount?",
                "answer": (
                    "The minimum deposit varies by product, "
                    "starting from ₸50,000."
                ),
                "category": "Deposits",
                "order": 1,
            },
            {
                "question": "How do I contact support?",
                "answer": (
                    "You can reach us via the app chat, email "
                    "support@rocketbank.company, or call our "
                    "hotline."
                ),
                "category": "Support",
                "order": 1,
            },
            {
                "question": "Is my money safe?",
                "answer": (
                    "All deposits up to ₸20,000,000 are insured "
                    "by the Kazakhstan Deposit Insurance Fund."
                ),
                "category": "General",
                "order": 1,
            },
            {
                "question": "How do I reset my password?",
                "answer": (
                    "Use the 'Forgot Password' link on the login "
                    "page or contact support."
                ),
                "category": "Security",
                "order": 1,
            },
            {
                "question": "What transfer limits apply?",
                "answer": (
                    "Daily transfer limits depend on your account "
                    "type and verification status."
                ),
                "category": "Transfers",
                "order": 1,
            },
        ]
        count = 0
        for data in faqs_data:
            _, created = FAQ.objects.get_or_create(
                question=data["question"],
                defaults=data,
            )
            if created:
                count += 1

        self.stdout.write(f"  Created {count} FAQs")

    def _generate_iban(self) -> str:
        """Generate a random IBAN."""
        bban = "".join(
            [str(random.randint(0, 9)) for _ in range(16)]
        )
        return f"KZ{random.randint(10, 99)}{bban}"

    def _create_bank_accounts(
        self, users: list, currencies: list
    ) -> list:
        """Create bank accounts for users."""
        accounts = []
        account_types = [
            BankAccount.AccountType.CHECKING,
            BankAccount.AccountType.SAVINGS,
        ]

        for user in users:
            for acc_type in account_types:
                for currency in currencies[:2]:  # KZT and USD
                    # Check for existing to avoid constraint
                    existing = BankAccount.all_objects.filter(
                        owner=user,
                        currency=currency,
                        account_type=acc_type,
                    ).first()
                    if existing:
                        accounts.append(existing)
                        continue

                    balance = Decimal(
                        str(
                            random.randint(10000, 5000000)
                        )
                    )
                    account = BankAccount(
                        owner=user,
                        currency=currency,
                        iban=self._generate_iban(),
                        account_type=acc_type,
                        balance=balance,
                        status=random.choice(
                            [
                                BankAccount.AccountStatus.ACTIVE,
                                BankAccount.AccountStatus.ACTIVE,
                                BankAccount.AccountStatus.ACTIVE,
                                BankAccount.AccountStatus.FROZEN,
                            ]
                        ),
                    )
                    account.save()
                    accounts.append(account)

        self.stdout.write(
            f"  Created {len(accounts)} bank accounts"
        )
        return accounts

    def _create_bank_cards(
        self,
        accounts: list,
        card_products: list,
    ) -> list:
        """Create bank cards for accounts."""
        cards = []
        for account in accounts[:40]:
            product = random.choice(card_products)
            last4 = f"{random.randint(1000, 9999)}"
            masked = f"**** **** **** {last4}"

            # Avoid duplicate
            if BankCard.objects.filter(
                account=account,
                card_number_masked=masked,
            ).exists():
                continue

            card = BankCard(
                account=account,
                product=product,
                card_number_masked=masked,
                expiry_date=(
                    timezone.now().date()
                    + timedelta(days=random.randint(365, 1825))
                ),
                status=BankCard.CardStatus.ACTIVE,
                daily_limit=Decimal(
                    str(
                        random.choice(
                            [100000, 250000, 500000, 1000000]
                        )
                    )
                ),
            )
            card.save()
            cards.append(card)

        self.stdout.write(
            f"  Created {len(cards)} bank cards"
        )
        return cards

    def _create_transactions(
        self,
        accounts: list,
        currencies: list,
        categories: list,
    ) -> list:
        """Create transaction records (150+ transactions)."""
        transactions = []
        kzt = currencies[0]  # KZT

        active_accounts = [
            a
            for a in accounts
            if a.status == BankAccount.AccountStatus.ACTIVE
        ]

        for i in range(160):
            sender = random.choice(active_accounts)
            receiver = random.choice(
                [a for a in active_accounts if a != sender]
            )
            amount = Decimal(
                str(random.randint(100, 500000))
            )
            ref = f"TXN-{uuid.uuid4().hex[:12].upper()}"

            txn = Transaction(
                sender_account=sender,
                receiver_account=receiver,
                amount=amount,
                currency=kzt,
                status=random.choice(
                    [
                        Transaction.TransactionStatus.COMPLETED,
                        Transaction.TransactionStatus.COMPLETED,
                        Transaction.TransactionStatus.COMPLETED,
                        Transaction.TransactionStatus.PENDING,
                        Transaction.TransactionStatus.FAILED,
                    ]
                ),
                transaction_type=random.choice(
                    [
                        Transaction.TransactionType.TRANSFER,
                        Transaction.TransactionType.PAYMENT,
                    ]
                ),
                description=fake.sentence(nb_words=6),
                reference_number=ref,
                category=random.choice(categories),
            )
            txn.save()
            transactions.append(txn)

        self.stdout.write(
            f"  Created {len(transactions)} transactions"
        )
        return transactions

    def _create_loans(
        self, users: list, loan_products: list
    ) -> list:
        """Create loan applications with schedules."""
        loans = []

        for user in users[:10]:
            product = random.choice(loan_products)
            amount = Decimal(
                str(
                    random.randint(
                        int(product.min_amount),
                        int(product.max_amount) // 2,
                    )
                )
            )
            term = random.randint(
                product.min_term_months,
                min(product.max_term_months, 36),
            )
            status = random.choice(
                [
                    LoanApplication.LoanStatus.APPROVED,
                    LoanApplication.LoanStatus.DISBURSED,
                    LoanApplication.LoanStatus.SUBMITTED,
                    LoanApplication.LoanStatus.UNDER_REVIEW,
                ]
            )

            loan = LoanApplication(
                user=user,
                product=product,
                requested_amount=amount,
                term_months=term,
                status=status,
                monthly_income=Decimal(
                    str(random.randint(200000, 2000000))
                ),
                approved_at=(
                    timezone.now() - timedelta(days=30)
                    if status
                    in [
                        LoanApplication.LoanStatus.APPROVED,
                        LoanApplication.LoanStatus.DISBURSED,
                    ]
                    else None
                ),
            )
            loan.save()
            loans.append(loan)

            # Create schedule for approved/disbursed loans
            if status in [
                LoanApplication.LoanStatus.APPROVED,
                LoanApplication.LoanStatus.DISBURSED,
            ]:
                self._generate_schedule(loan)

        self.stdout.write(
            f"  Created {len(loans)} loan applications"
        )
        return loans

    def _generate_schedule(self, loan: LoanApplication):
        """Generate simple amortization schedule for a loan."""
        monthly_rate = (
            loan.product.interest_rate
            / Decimal("100")
            / Decimal("12")
        )
        remaining = loan.requested_amount
        monthly_payment = (
            remaining / loan.term_months
        ) + (remaining * monthly_rate)
        start = timezone.now().date()

        entries = []
        for i in range(1, loan.term_months + 1):
            interest = (remaining * monthly_rate).quantize(
                Decimal("0.01")
            )
            principal = min(
                monthly_payment - interest, remaining
            )
            if principal < 0:
                principal = Decimal("0")

            entry = LoanSchedule(
                loan=loan,
                installment_number=i,
                due_date=start + timedelta(days=30 * i),
                principal_amount=principal.quantize(
                    Decimal("0.01")
                ),
                interest_amount=interest,
                is_paid=i <= 3,  # First 3 paid
                paid_at=(
                    timezone.now() - timedelta(days=30 * (4 - i))
                    if i <= 3
                    else None
                ),
            )
            entries.append(entry)
            remaining -= principal

        LoanSchedule.objects.bulk_create(entries)

    def _create_deposits(
        self,
        users: list,
        accounts: list,
        deposit_products: list,
    ) -> list:
        """Create user deposits."""
        deposits = []
        active_accounts = [
            a
            for a in accounts
            if a.status == BankAccount.AccountStatus.ACTIVE
        ]

        for user in users[:10]:
            user_accounts = [
                a for a in active_accounts if a.owner == user
            ]
            if not user_accounts:
                continue

            product = random.choice(deposit_products)
            account = random.choice(user_accounts)
            amount = Decimal(
                str(random.randint(100000, 5000000))
            )
            start = timezone.now().date() - timedelta(
                days=random.randint(30, 365)
            )

            dep = UserDeposit(
                user=user,
                account=account,
                product=product,
                amount=amount,
                accrued_interest=(
                    amount
                    * product.interest_rate
                    / Decimal("100")
                    / Decimal("12")
                ).quantize(Decimal("0.01")),
                start_date=start,
                end_date=start
                + timedelta(days=30 * product.term_months),
                status=UserDeposit.DepositStatus.ACTIVE,
            )
            dep.save()
            deposits.append(dep)

        self.stdout.write(
            f"  Created {len(deposits)} user deposits"
        )
        return deposits

    def _create_saving_goals(self, users: list):
        """Create saving goals for users."""
        categories = [
            "vacation",
            "car",
            "house",
            "education",
            "emergency",
        ]
        goals = []
        for user in users[:10]:
            target = Decimal(
                str(random.randint(500000, 10000000))
            )
            current = Decimal(
                str(random.randint(0, int(target)))
            )
            goal = SavingGoal(
                user=user,
                title=fake.sentence(nb_words=3),
                target_amount=target,
                current_amount=current,
                deadline=timezone.now().date()
                + timedelta(days=random.randint(90, 730)),
                category=random.choice(categories),
                is_achieved=current >= target,
            )
            goal.save()
            goals.append(goal)

        self.stdout.write(
            f"  Created {len(goals)} saving goals"
        )

    def _create_notifications(self, users: list):
        """Create notifications for users."""
        count = 0
        types = [
            Notification.NotificationType.INFO,
            Notification.NotificationType.SUCCESS,
            Notification.NotificationType.WARNING,
            Notification.NotificationType.TRANSACTION,
            Notification.NotificationType.SECURITY,
        ]

        for user in users:
            for _ in range(random.randint(3, 8)):
                Notification.objects.create(
                    user=user,
                    title=fake.sentence(nb_words=4),
                    message=fake.paragraph(nb_sentences=2),
                    notification_type=random.choice(types),
                    is_read=random.choice([True, False]),
                )
                count += 1

        self.stdout.write(
            f"  Created {count} notifications"
        )

    def _create_support_tickets(self, users: list):
        """Create support tickets with reviews."""
        tickets = []
        priorities = [
            SupportTicket.TicketPriority.LOW,
            SupportTicket.TicketPriority.MEDIUM,
            SupportTicket.TicketPriority.HIGH,
            SupportTicket.TicketPriority.URGENT,
        ]
        statuses = [
            SupportTicket.TicketStatus.OPEN,
            SupportTicket.TicketStatus.IN_PROGRESS,
            SupportTicket.TicketStatus.RESOLVED,
            SupportTicket.TicketStatus.CLOSED,
        ]

        for user in users[:10]:
            for _ in range(random.randint(1, 3)):
                ticket = SupportTicket.objects.create(
                    user=user,
                    subject=fake.sentence(nb_words=5),
                    description=fake.paragraph(nb_sentences=3),
                    status=random.choice(statuses),
                    priority=random.choice(priorities),
                )
                tickets.append(ticket)

                # Add review for resolved/closed tickets
                if ticket.status in [
                    SupportTicket.TicketStatus.RESOLVED,
                    SupportTicket.TicketStatus.CLOSED,
                ]:
                    TicketReview.objects.create(
                        ticket=ticket,
                        user=user,
                        rating=random.randint(1, 5),
                        comment=fake.sentence(nb_words=8),
                    )

        self.stdout.write(
            f"  Created {len(tickets)} support tickets"
        )

    def _create_beneficiaries(
        self, users: list, accounts: list
    ):
        """Create beneficiaries for users."""
        count = 0
        for user in users[:10]:
            user_accounts = [
                a for a in accounts if a.owner != user
            ]
            for _ in range(random.randint(1, 3)):
                if not user_accounts:
                    break
                target = random.choice(user_accounts)
                ben, created = Beneficiary.objects.get_or_create(
                    owner=user,
                    account=target,
                )
                if created:
                    SavedBeneficiary.objects.create(
                        beneficiary=ben,
                        nickname=fake.first_name(),
                        is_favorite=random.choice(
                            [True, False]
                        ),
                    )
                    count += 1

        self.stdout.write(
            f"  Created {count} beneficiaries"
        )
