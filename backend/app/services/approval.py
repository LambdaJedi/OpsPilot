
from decimal import Decimal

from backend.app.models.purchase_request import ApprovalRoute


def determine_approval_route(amount: Decimal) -> ApprovalRoute:
    """
    Determine the approval route based on the purchase amount.
    """

    if not amount.is_finite() or amount <= Decimal("0"):
        raise ValueError("Purchase amount must be greater than zero.")

    if amount < Decimal("2000"):
        return ApprovalRoute.AUTOMATIC_ELIGIBILITY

    if amount < Decimal("20000"):
        return ApprovalRoute.MANAGER

    return ApprovalRoute.MANAGER_AND_FINANCE
