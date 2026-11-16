
from decimal import Decimal

import pytest

from backend.app.services.approval import (
    ApprovalRoute,
    determine_approval_route,
)


@pytest.mark.parametrize(
    "amount, expected_route",
    [
        (Decimal("500"), ApprovalRoute.AUTOMATIC_ELIGIBILITY),
        (Decimal("1999.99"), ApprovalRoute.AUTOMATIC_ELIGIBILITY),
        (Decimal("2000"), ApprovalRoute.MANAGER),
        (Decimal("18500"), ApprovalRoute.MANAGER),
        (Decimal("19999.99"), ApprovalRoute.MANAGER),
        (Decimal("20000"), ApprovalRoute.MANAGER_AND_FINANCE),
        (Decimal("50000"), ApprovalRoute.MANAGER_AND_FINANCE),
    ],
)
def test_determine_approval_route(amount, expected_route):
    assert determine_approval_route(amount) == expected_route


@pytest.mark.parametrize(
    "amount",
    [
        Decimal("0"),
        Decimal("-100"),
    ],
)
def test_invalid_purchase_amount(amount):
    with pytest.raises(ValueError):
        determine_approval_route(amount)
