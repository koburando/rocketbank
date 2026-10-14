"""
Business logic / service layer for the Credits app.

Handles annuity loan payment calculation and schedule generation.
"""

import logging
from datetime import timedelta
from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction
from django.utils import timezone

from apps.credits.models import LoanApplication, LoanSchedule

logger = logging.getLogger(__name__)


def calculate_annuity_payment(
    principal: Decimal,
    annual_rate: Decimal,
    term_months: int,
) -> Decimal:
    """
    Calculate monthly annuity payment using the standard formula.

    A = P * [r(1+r)^n] / [(1+r)^n - 1]

    Args:
        principal: Loan principal amount.
        annual_rate: Annual interest rate as percentage (e.g. 12.5).
        term_months: Loan term in months.

    Returns:
        Monthly payment amount rounded to 2 decimal places.
    """
    if annual_rate == 0:
        return (principal / term_months).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    monthly_rate = annual_rate / Decimal("100") / Decimal("12")
    power = (1 + monthly_rate) ** term_months
    payment = principal * (monthly_rate * power) / (power - 1)
    return payment.quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


@transaction.atomic
def generate_loan_schedule(
    loan_application: LoanApplication,
) -> list[LoanSchedule]:
    """
    Generate a full amortization schedule for a loan application.

    Creates LoanSchedule entries for each monthly installment
    with principal and interest breakdown.

    Args:
        loan_application: The approved LoanApplication instance.

    Returns:
        List of created LoanSchedule instances.
    """
    # Clear existing schedule if regenerating
    loan_application.schedule_entries.all().delete()

    principal = loan_application.requested_amount
    annual_rate = loan_application.product.interest_rate
    term = loan_application.term_months

    monthly_payment = calculate_annuity_payment(
        principal, annual_rate, term
    )
    monthly_rate = annual_rate / Decimal("100") / Decimal("12")

    remaining_principal = principal
    start_date = timezone.now().date()
    schedule_entries = []

    for i in range(1, term + 1):
        interest = (remaining_principal * monthly_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        principal_part = monthly_payment - interest

        # Last installment adjustment
        if i == term:
            principal_part = remaining_principal
            interest = monthly_payment - principal_part
            if interest < 0:
                interest = Decimal("0")

        due_date = start_date + timedelta(days=30 * i)

        entry = LoanSchedule(
            loan=loan_application,
            installment_number=i,
            due_date=due_date,
            principal_amount=principal_part,
            interest_amount=interest,
        )
        schedule_entries.append(entry)
        remaining_principal -= principal_part

    LoanSchedule.objects.bulk_create(schedule_entries)

    logger.info(
        "Generated %d schedule entries for loan #%s",
        len(schedule_entries),
        loan_application.pk,
    )
    return schedule_entries


@transaction.atomic
def approve_loan(
    loan_application: LoanApplication,
) -> LoanApplication:
    """
    Approve a loan application and generate its schedule.

    Args:
        loan_application: The LoanApplication to approve.

    Returns:
        Updated LoanApplication with APPROVED status.
    """
    loan_application.status = LoanApplication.LoanStatus.APPROVED
    loan_application.approved_at = timezone.now()
    loan_application.save(
        update_fields=["status", "approved_at", "updated_at"]
    )
    generate_loan_schedule(loan_application)

    logger.info("Approved loan #%s", loan_application.pk)
    return loan_application
