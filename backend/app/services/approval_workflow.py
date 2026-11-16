
from sqlalchemy.orm import Session

from backend.app.models.approval import (
    Approval,
    ApprovalDecision,
    ApprovalRole,
)
from backend.app.models.purchase_request import (
    ApprovalRoute,
    PurchaseRequest,
)


def create_approval_records(
    db: Session,
    purchase_request: PurchaseRequest,
) -> None:
    """
    Create the approval records required by a purchase request.

    MANAGER:
        Requires one manager approval.

    MANAGER_AND_FINANCE:
        Requires both manager and finance approvals.

    AUTOMATIC_ELIGIBILITY:
        Does not create manual approval records yet.
        Automatic policy checks will be implemented separately.
    """

    approval_roles = []

    if purchase_request.approval_route == ApprovalRoute.MANAGER:
        approval_roles = [ApprovalRole.MANAGER]

    elif purchase_request.approval_route == ApprovalRoute.MANAGER_AND_FINANCE:
        approval_roles = [
            ApprovalRole.MANAGER,
            ApprovalRole.FINANCE,
        ]

    approvals = [
        Approval(
            request_id=purchase_request.id,
            approval_role=role,
            decision=ApprovalDecision.PENDING,
        )
        for role in approval_roles
    ]

    db.add_all(approvals)
