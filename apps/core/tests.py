from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import BankAccount, Currency
from apps.cards.models import BankCard, CardProduct
from apps.core.converters import IBANConverter, ReferenceConverter
from apps.core.templatetags.bank_tags import currency_format, mask_iban, status_badge_class
from apps.credits.models import LoanProduct
from apps.deposits.models import DepositProduct
from apps.notifications.models import Notification
from apps.support.models import FAQ, SupportTicket

User = get_user_model()


class ConvertersTestCase(TestCase):
    def test_iban_converter(self):
        conv = IBANConverter()
        valid_iban = "KZ123456789012345678"
        self.assertEqual(conv.to_python(valid_iban), valid_iban)
        self.assertEqual(conv.to_url(valid_iban), valid_iban)

    def test_reference_converter(self):
        conv = ReferenceConverter()
        valid_ref = "TXN-2026-ABCD1234EF"
        self.assertEqual(conv.to_python(valid_ref), valid_ref)
        self.assertEqual(conv.to_url(valid_ref), valid_ref)


class TemplateTagsTestCase(TestCase):
    def test_mask_iban(self):
        iban = "KZ123456789012345678"
        masked = mask_iban(iban)
        self.assertTrue(masked.startswith("KZ12"))
        self.assertTrue(masked.endswith("5678"))
        self.assertIn("••••", masked)
        self.assertEqual(mask_iban(""), "")

    def test_currency_format(self):
        formatted = currency_format(Decimal("1250000.50"), "KZT")
        self.assertIn("1,250,000.50", formatted)
        self.assertIn("₸", formatted)

        usd_formatted = currency_format(100, "USD")
        self.assertIn("$", usd_formatted)

    def test_status_badge_class(self):
        self.assertEqual(status_badge_class("ACTIVE"), "badge--success")
        self.assertEqual(status_badge_class("COMPLETED"), "badge--success")
        self.assertEqual(status_badge_class("BLOCKED"), "badge--danger")
        self.assertEqual(status_badge_class("REJECTED"), "badge--danger")
        self.assertEqual(status_badge_class("PENDING"), "badge--warning")
        self.assertEqual(status_badge_class("UNKNOWN"), "badge--secondary")


class PublicViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.currency = Currency.objects.create(
            code="KZT",
            name="Kazakhstani Tenge",
            symbol="₸",
            is_active=True,
        )
        self.card_prod = CardProduct.objects.create(
            title="Rocket Black",
            slug="rocket-black",
            tier=CardProduct.CardTier.BLACK,
            description="Premium debit card with 5% cashback",
            annual_fee=Decimal("0.00"),
            cashback_percent=Decimal("5.00"),
            is_active=True,
        )
        self.loan_prod = LoanProduct.objects.create(
            title="Rocket Consumer Credit",
            slug="rocket-consumer",
            min_amount=Decimal("50000"),
            max_amount=Decimal("5000000"),
            interest_rate=Decimal("14.50"),
            min_term_months=6,
            max_term_months=60,
            is_active=True,
        )
        self.deposit_prod = DepositProduct.objects.create(
            title="Rocket Savings Boost",
            slug="rocket-savings-boost",
            interest_rate=Decimal("15.50"),
            min_amount=Decimal("10000"),
            term_months=12,
            is_active=True,
        )
        self.faq = FAQ.objects.create(
            question="How do I freeze my Rocket card?",
            answer="Go to Cards management and click freeze.",
            category="CARDS",
            is_published=True,
            order=1,
        )

    def test_landing_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertIn("X-Request-Duration-Ms", response.headers)

    def test_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

    def test_contacts_page(self):
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts.html")

    def test_robots_txt(self):
        response = self.client.get(reverse("robots-txt"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")

    def test_sitemap_xml(self):
        response = self.client.get(reverse("django.contrib.sitemaps.views.sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/xml", response["Content-Type"])

    def test_card_catalog_and_detail(self):
        catalog_res = self.client.get(reverse("cards:catalog"))
        self.assertEqual(catalog_res.status_code, 200)
        self.assertTemplateUsed(catalog_res, "cards/catalog.html")

        detail_res = self.client.get(reverse("cards:detail", kwargs={"slug": self.card_prod.slug}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertTemplateUsed(detail_res, "cards/detail.html")

    def test_credits_catalog_detail_and_calculator(self):
        catalog_res = self.client.get(reverse("credits:catalog"))
        self.assertEqual(catalog_res.status_code, 200)
        self.assertTemplateUsed(catalog_res, "credits/catalog.html")

        detail_res = self.client.get(
            reverse("credits:detail", kwargs={"slug": self.loan_prod.slug})
        )
        self.assertEqual(detail_res.status_code, 200)
        self.assertTemplateUsed(detail_res, "credits/detail.html")

        calc_res = self.client.get(reverse("credits:calculator"))
        self.assertEqual(calc_res.status_code, 200)
        self.assertTemplateUsed(calc_res, "credits/loan_calculator.html")

    def test_deposits_catalog(self):
        response = self.client.get(reverse("deposits:catalog"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "deposits/catalog.html")

    def test_faq_page(self):
        response = self.client.get(reverse("support:faq"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "support/faq.html")

    def test_auth_pages_public(self):
        login_res = self.client.get(reverse("users:login"))
        self.assertEqual(login_res.status_code, 200)
        self.assertTemplateUsed(login_res, "users/login.html")

        register_res = self.client.get(reverse("users:register"))
        self.assertEqual(register_res.status_code, 200)
        self.assertTemplateUsed(register_res, "users/register.html")

        reset_res = self.client.get(reverse("users:password-reset"))
        self.assertEqual(reset_res.status_code, 200)
        self.assertTemplateUsed(reset_res, "users/password_reset.html")

    def test_custom_404_page(self):
        response = self.client.get("/non-existent-bank-route-404/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")


class AuthenticatedViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="astana_client",
            email="client@rocketbank.kz",
            password="StrongPassword123!",
            first_name="Almas",
            last_name="Serikov",
            is_verified=True,
        )
        self.currency = Currency.objects.create(
            code="KZT",
            name="Kazakhstani Tenge",
            symbol="₸",
            is_active=True,
        )
        self.account = BankAccount.objects.create(
            owner=self.user,
            currency=self.currency,
            account_type=BankAccount.AccountType.CHECKING,
            balance=Decimal("250000.00"),
            iban="KZ999999999999999999",
            status=BankAccount.AccountStatus.ACTIVE,
        )
        self.card_prod = CardProduct.objects.create(
            title="Rocket Metal",
            slug="rocket-metal",
            tier=CardProduct.CardTier.PLATINUM,
            description="Luxury metal card",
            annual_fee=Decimal("12000.00"),
            cashback_percent=Decimal("7.00"),
            is_active=True,
        )
        self.card = BankCard.objects.create(
            account=self.account,
            product=self.card_prod,
            card_number_masked="5412••••••••9876",
            expiry_date=date.today() + timedelta(days=365 * 3),
            status=BankCard.CardStatus.ACTIVE,
        )
        self.notification = Notification.objects.create(
            user=self.user,
            title="Welcome to RocketBank",
            message="Your account is fully operational.",
            notification_type="SYSTEM",
            is_read=False,
        )
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            subject="Card delivery question",
            description="When will my physical card arrive in Astana?",
            priority=SupportTicket.TicketPriority.MEDIUM,
            status=SupportTicket.TicketStatus.OPEN,
        )
        self.client.force_login(self.user)

    def test_dashboard_view(self):
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/dashboard.html")
        self.assertEqual(len(response.context["accounts"]), 1)

    def test_account_views(self):
        list_res = self.client.get(reverse("accounts:list"))
        self.assertEqual(list_res.status_code, 200)
        self.assertTemplateUsed(list_res, "accounts/account_list.html")

        detail_res = self.client.get(reverse("accounts:detail", kwargs={"pk": self.account.pk}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertTemplateUsed(detail_res, "accounts/account_detail.html")

        detail_iban_res = self.client.get(
            reverse("accounts:detail-by-iban", kwargs={"iban": self.account.iban})
        )
        self.assertEqual(detail_iban_res.status_code, 200)
        self.assertTemplateUsed(detail_iban_res, "accounts/account_detail.html")

        open_res = self.client.get(reverse("accounts:open"))
        self.assertEqual(open_res.status_code, 200)
        self.assertTemplateUsed(open_res, "accounts/account_open.html")

        beneficiaries_res = self.client.get(reverse("accounts:beneficiaries"))
        self.assertEqual(beneficiaries_res.status_code, 200)
        self.assertTemplateUsed(beneficiaries_res, "accounts/beneficiaries.html")

    def test_transaction_views(self):
        transfer_res = self.client.get(reverse("transactions:transfer"))
        self.assertEqual(transfer_res.status_code, 200)
        self.assertTemplateUsed(transfer_res, "transactions/transfer.html")

        history_res = self.client.get(reverse("transactions:list"))
        self.assertEqual(history_res.status_code, 200)
        self.assertTemplateUsed(history_res, "transactions/transaction_list.html")

    def test_card_management_and_toggle_freeze(self):
        list_res = self.client.get(reverse("cards:list"))
        self.assertEqual(list_res.status_code, 200)
        self.assertTemplateUsed(list_res, "cards/card_list.html")

        wizard_res = self.client.get(reverse("cards:apply"))
        self.assertEqual(wizard_res.status_code, 200)
        self.assertTemplateUsed(wizard_res, "cards/card_apply_wizard.html")

        # Freeze FBV
        freeze_res = self.client.post(
            reverse("cards:toggle-freeze", kwargs={"pk": self.card.pk}),
            follow=True,
        )
        self.assertEqual(freeze_res.status_code, 200)
        self.card.refresh_from_db()
        self.assertEqual(self.card.status, BankCard.CardStatus.BLOCKED)

    def test_credit_and_deposit_views(self):
        loans_res = self.client.get(reverse("credits:list"))
        self.assertEqual(loans_res.status_code, 200)
        self.assertTemplateUsed(loans_res, "credits/loan_list.html")

        apply_res = self.client.get(reverse("credits:apply"))
        self.assertEqual(apply_res.status_code, 200)
        self.assertTemplateUsed(apply_res, "credits/loan_apply.html")

        deposits_res = self.client.get(reverse("deposits:list"))
        self.assertEqual(deposits_res.status_code, 200)
        self.assertTemplateUsed(deposits_res, "deposits/deposit_list.html")

        open_res = self.client.get(reverse("deposits:open"))
        self.assertEqual(open_res.status_code, 200)
        self.assertTemplateUsed(open_res, "deposits/deposit_open.html")

    def test_analytics_and_notifications(self):
        analytics_res = self.client.get(reverse("analytics:dashboard"))
        self.assertEqual(analytics_res.status_code, 200)
        self.assertTemplateUsed(analytics_res, "analytics/dashboard.html")

        notif_res = self.client.get(reverse("notifications:list"))
        self.assertEqual(notif_res.status_code, 200)
        self.assertTemplateUsed(notif_res, "notifications/notification_list.html")

        # Mark read FBV
        read_res = self.client.post(
            reverse("notifications:mark-read", kwargs={"pk": self.notification.pk}),
            follow=True,
        )
        self.assertEqual(read_res.status_code, 200)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_support_tickets_views(self):
        list_res = self.client.get(reverse("support:list"))
        self.assertEqual(list_res.status_code, 200)
        self.assertTemplateUsed(list_res, "support/ticket_list.html")

        create_res = self.client.get(reverse("support:create"))
        self.assertEqual(create_res.status_code, 200)
        self.assertTemplateUsed(create_res, "support/ticket_create.html")

        detail_res = self.client.get(reverse("support:detail", kwargs={"pk": self.ticket.pk}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertTemplateUsed(detail_res, "support/ticket_detail.html")

    def test_user_profile_security_and_kyc(self):
        prof_res = self.client.get(reverse("users:profile"))
        self.assertEqual(prof_res.status_code, 200)
        self.assertTemplateUsed(prof_res, "users/profile.html")

        sec_res = self.client.get(reverse("users:security"))
        self.assertEqual(sec_res.status_code, 200)
        self.assertTemplateUsed(sec_res, "users/security.html")

        kyc_res = self.client.get(reverse("users:kyc-upload"))
        self.assertEqual(kyc_res.status_code, 200)
        self.assertTemplateUsed(kyc_res, "users/kyc_upload.html")

    def test_owner_required_mixin_forbidden(self):
        other_user = User.objects.create_user(
            username="other_person",
            email="other@bank.kz",
            password="OtherPassword123!",
        )
        self.client.force_login(other_user)

        # Trying to access self.account belonging to astana_client
        res = self.client.get(reverse("accounts:detail", kwargs={"pk": self.account.pk}))
        self.assertEqual(res.status_code, 403)
        self.assertTemplateUsed(res, "403.html")

        # Trying to access self.ticket belonging to astana_client
        res_ticket = self.client.get(reverse("support:detail", kwargs={"pk": self.ticket.pk}))
        self.assertEqual(res_ticket.status_code, 403)
        self.assertTemplateUsed(res_ticket, "403.html")

    def test_logout_post_only(self):
        # GET should be rejected with 405 Method Not Allowed
        get_res = self.client.get(reverse("users:logout"))
        self.assertEqual(get_res.status_code, 405)

        # POST should successfully log out and redirect
        post_res = self.client.post(reverse("users:logout"))
        self.assertEqual(post_res.status_code, 302)
        self.assertFalse(self.client.session.get("_auth_user_id"))


class LanguageSwitchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_switch_language_ru(self):
        response = self.client.get(reverse("switch_language", kwargs={"lang_code": "ru"}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies.get("django_language").value, "ru")
        page = self.client.get(reverse("about"))
        self.assertEqual(page.status_code, 200)
        self.assertIn("О банке", page.content.decode("utf-8"))

    def test_switch_language_kk(self):
        response = self.client.get(reverse("switch_language", kwargs={"lang_code": "kk"}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies.get("django_language").value, "kk")
        page = self.client.get(reverse("about"))
        self.assertEqual(page.status_code, 200)
        self.assertIn("Банк туралы", page.content.decode("utf-8"))

    def test_switch_language_en(self):
        response = self.client.get(reverse("switch_language", kwargs={"lang_code": "en"}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies.get("django_language").value, "en")
        page = self.client.get(reverse("about"))
        self.assertEqual(page.status_code, 200)
        self.assertIn("About RocketBank", page.content.decode("utf-8"))

    def test_switch_language_invalid_fallback(self):
        response = self.client.get(reverse("switch_language", kwargs={"lang_code": "fr"}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies.get("django_language").value, "ru")

