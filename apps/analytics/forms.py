"""
Forms and Formsets for the Analytics and Saving Goals app.
"""

from django import forms
from django.forms import modelformset_factory

from apps.analytics.models import SavingGoal


class SavingGoalForm(forms.ModelForm):
    """
    Form for creating or updating a saving goal.
    """

    class Meta:
        model = SavingGoal
        fields = ["title", "target_amount", "current_amount", "deadline", "category"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "e.g. New Electric Car",
                    "required": "required",
                }
            ),
            "target_amount": forms.NumberInput(
                attrs={
                    "class": "form-input font-mono",
                    "placeholder": "1000000",
                    "min": "1000",
                    "step": "1000",
                    "required": "required",
                }
            ),
            "current_amount": forms.NumberInput(
                attrs={
                    "class": "form-input font-mono",
                    "placeholder": "250000",
                    "min": "0",
                    "step": "1000",
                }
            ),
            "deadline": forms.DateInput(
                attrs={"class": "form-input", "type": "date"}
            ),
            "category": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "e.g. vacation, car, house"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get("target_amount")
        current = cleaned_data.get("current_amount")
        if target is not None and current is not None:
            if current > target:
                cleaned_data["is_achieved"] = True
        return cleaned_data


SavingGoalFormSet = modelformset_factory(
    SavingGoal,
    form=SavingGoalForm,
    extra=1,
    can_delete=True,
)
