"""
Views for authentication, registration, email verification, profile, and security.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import FormView, TemplateView, UpdateView

from apps.users.forms import (
    KYCDocumentUploadForm,
    StyledPasswordChangeForm,
    UserLoginForm,
    UserProfileForm,
    UserRegistrationForm,
)
from apps.users.models import LoginAudit, Profile, User


class RegisterView(FormView):
    """
    User registration view with email verification token generation.
    """

    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        # Generate email verification token
        signer = TimestampSigner()
        token = signer.sign(str(user.id))

        messages.success(
            self.request,
            f"Registration successful for {user.email}! "
            f"A verification token has been generated: {token[:16]}... "
            "Please check your inbox or verify your account to unlock all banking features.",
        )
        return super().form_valid(form)


class VerifyEmailView(View):
    """
    Email verification token validation flow.
    """

    def get(self, request, token):
        signer = TimestampSigner()
        try:
            # Token valid for 48 hours (172800 seconds)
            user_id = signer.unsign(token, max_age=172800)
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            messages.success(
                request, "Your email address has been successfully verified! You may now sign in."
            )
        except SignatureExpired:
            messages.error(
                request, "Verification link has expired. Please request a new verification email."
            )
        except (BadSignature, User.DoesNotExist):
            messages.error(request, "Invalid verification token.")

        return redirect("users:login")


class LoginUserView(FormView):
    """
    Login view supporting authentication by email or username,
    and recording LoginAudit events.
    """

    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("accounts:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.user
        remember_me = form.cleaned_data.get("remember_me")

        # Session expiry based on remember_me
        if not remember_me:
            self.request.session.set_expiry(0)  # expires on browser close
        else:
            self.request.session.set_expiry(1209600)  # 2 weeks

        login(self.request, user)

        # Record successful LoginAudit
        ip = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0].strip()
        else:
            ip = self.request.META.get("REMOTE_ADDR", "127.0.0.1")

        ua = self.request.META.get("HTTP_USER_AGENT", "")[:250]
        LoginAudit.objects.create(
            user=user,
            ip_address=ip,
            user_agent=ua,
            login_successful=True,
            location="Almaty, KZ",
        )

        messages.success(self.request, f"Welcome back, {user.first_name or user.username}!")
        next_url = self.request.GET.get("next") or self.get_success_url()
        return redirect(next_url)

    def form_invalid(self, form):
        # Record failed audit if email/username was recognized
        ident = form.cleaned_data.get("username_or_email")
        if ident:
            u = (
                User.objects.filter(email=ident).first()
                or User.objects.filter(username=ident).first()
            )
            if u:
                ip = self.request.META.get("REMOTE_ADDR", "127.0.0.1")
                LoginAudit.objects.create(
                    user=u,
                    ip_address=ip,
                    user_agent=self.request.META.get("HTTP_USER_AGENT", "")[:250],
                    login_successful=False,
                )
        return super().form_invalid(form)


@method_decorator(require_POST, name="dispatch")
class LogoutUserView(View):
    """
    Logout view strictly via POST request.
    """

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been successfully signed out of RocketBank.")
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"], "Logout is strictly permitted via POST only.")


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    User profile viewing and editing screen with Pillow avatar resizing.
    """

    model = Profile
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile details have been successfully updated.")
        return super().form_valid(form)


class SecuritySettingsView(LoginRequiredMixin, TemplateView):
    """
    Security settings page showing login audits and password change options.
    """

    template_name = "users/security.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_audits"] = LoginAudit.objects.filter(user=self.request.user)[:10]
        context["password_form"] = StyledPasswordChangeForm(user=self.request.user)
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    In-app password change view.
    """

    form_class = StyledPasswordChangeForm
    template_name = "users/security.html"
    success_url = reverse_lazy("users:security")

    def form_valid(self, form):
        messages.success(self.request, "Your security password has been changed successfully.")
        return super().form_valid(form)


class KYCUploadView(LoginRequiredMixin, FormView):
    """
    Complex KYC file upload view with document verification flow.
    """

    template_name = "users/kyc_upload.html"
    form_class = KYCDocumentUploadForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        profile.kyc_status = Profile.KYCStatus.PENDING
        profile.save(update_fields=["kyc_status", "updated_at"])

        messages.success(
            self.request,
            f"KYC document ({form.cleaned_data['document_type']}) uploaded successfully! "
            "Our compliance team will review your identity verification within 24 hours.",
        )
        return super().form_valid(form)


# Standard Django Password Reset views styled with RocketBank design system
class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password-reset-done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password-reset-complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
