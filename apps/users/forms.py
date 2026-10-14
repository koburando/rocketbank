"""
Forms for authentication, user profiles, security, and KYC verification.
"""

from io import BytesIO

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image

from apps.users.models import Profile

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    User registration form with email, username, password confirmation,
    and terms acceptance.
    """

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Enter a secure password",
                "autocomplete": "new-password",
                "required": "required",
                "minlength": "8",
            }
        ),
        help_text="Minimum 8 characters with letters and numbers.",
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Re-type password",
                "autocomplete": "new-password",
                "required": "required",
            }
        ),
    )
    accept_terms = forms.BooleanField(
        label="I agree to the Terms of Service and Privacy Policy",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = User
        fields = ["email", "username", "phone_number"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "name@example.com",
                    "autocomplete": "email",
                    "required": "required",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Unique username",
                    "autocomplete": "username",
                    "required": "required",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "+7 700 123 4567",
                    "type": "tel",
                    "autocomplete": "tel",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_verified = False  # requires email token verification
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class UserLoginForm(forms.Form):
    """
    Login form allowing authentication via email or username.
    """

    username_or_email = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "name@example.com or username",
                "autocomplete": "username",
                "required": "required",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "••••••••",
                "autocomplete": "current-password",
                "required": "required",
            }
        ),
    )
    remember_me = forms.BooleanField(
        label="Remember this device",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email", "").strip()
        password = cleaned_data.get("password", "")

        if username_or_email and password:
            # Check by email first, then username
            user = None
            if "@" in username_or_email:
                try:
                    u = User.objects.get(email=username_or_email.lower())
                    user = authenticate(username=u.email, password=password)
                except User.DoesNotExist:
                    pass

            if not user:
                user = authenticate(username=username_or_email, password=password)

            if not user:
                raise ValidationError("Invalid email/username or password. Please try again.")
            if not user.is_active:
                raise ValidationError("This user account is suspended or inactive.")
            self.user = user

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Profile edit form with avatar image upload and Pillow resize.
    """

    first_name = forms.CharField(
        label="First Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input", "autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input", "autocomplete": "family-name"}),
    )
    phone_number = forms.CharField(
        label="Phone Number",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input", "type": "tel", "autocomplete": "tel"}),
    )

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "birth_date",
            "address",
            "preferred_theme",
            "preferred_language",
        ]
        widgets = {
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-input",
                    "type": "file",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                    "autocomplete": "bday",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 3,
                    "placeholder": "Street address, City, Postal Code",
                    "autocomplete": "street-address",
                }
            ),
            "preferred_theme": forms.Select(attrs={"class": "form-select"}),
            "preferred_language": forms.Select(
                choices=[("en", "English"), ("kk", "Kazakh"), ("ru", "Russian")],
                attrs={"class": "form-select"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "user") and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["phone_number"].initial = self.instance.user.phone_number

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and hasattr(avatar, "size"):
            # Check max size 5MB
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError("Avatar image file size must not exceed 5 MB.")
            # Verify image file integrity with Pillow
            try:
                img = Image.open(avatar)
                img.verify()
            except Exception:
                raise ValidationError("Uploaded file is not a valid image.")
        return avatar

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.phone_number = self.cleaned_data.get("phone_number", "")
        user.save(update_fields=["first_name", "last_name", "phone_number"])

        avatar = self.cleaned_data.get("avatar")
        # Resize avatar via Pillow if new image provided
        if avatar and hasattr(avatar, "file"):
            try:
                img = Image.open(avatar)
                img = img.convert("RGB")
                max_size = (400, 400)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                buffer.seek(0)
                profile.avatar.save(f"avatar_{user.id}.jpg", ContentFile(buffer.read()), save=False)
            except Exception:
                pass

        if commit:
            profile.save()
        return profile


class KYCDocumentUploadForm(forms.Form):
    """
    Complex KYC file upload form with document type selection and image preview.
    """

    DOCUMENT_CHOICES = [
        ("PASSPORT", "National Passport"),
        ("ID_CARD", "Government National ID Card"),
        ("DRIVERS_LICENSE", "Driver's License"),
        ("RESIDENCE_PERMIT", "Residence Permit"),
    ]

    document_type = forms.ChoiceField(
        label="Document Type",
        choices=DOCUMENT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select", "required": "required"}),
    )
    document_number = forms.CharField(
        label="Document Number / ID",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "e.g. 123456789",
                "required": "required",
            }
        ),
    )
    document_file = forms.FileField(
        label="Upload Scanned Document or Photo (JPEG, PNG, WebP, PDF)",
        widget=forms.FileInput(
            attrs={
                "class": "form-input",
                "type": "file",
                "accept": "image/*,.pdf",
                "required": "required",
                "id": "kyc_file_input",
            }
        ),
        help_text="Clear color image, max 10MB. Text must be completely readable.",
    )
    consent_given = forms.BooleanField(
        label=(
            "I declare that all provided documents are genuine and authorize "
            "verification with government identity registries."
        ),
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean_document_file(self):
        file = self.cleaned_data.get("document_file")
        if file:
            if file.size > 10 * 1024 * 1024:
                raise ValidationError("Document file size must not exceed 10 MB.")
        return file


class StyledPasswordChangeForm(PasswordChangeForm):
    """
    Subclass of Django's PasswordChangeForm with design system styling.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-input"})
