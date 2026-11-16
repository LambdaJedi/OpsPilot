
from datetime import datetime, timezone
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.approval import (
    Approval,
    ApprovalDecision,
    ApprovalRole,
)
from backend.app.models.purchase_request import (
    ApprovalRoute,
    PurchaseRequest,
    RequestStatus,
)


class ApprovalWorkflowError(Exception):
    """Raised when an approval decision violates workflow rules."""


class RequestNotFoundError(ApprovalWorkflowError):
    pass


class ApprovalNotFoundError(ApprovalWorkflowError):
    pass


def process_approval_decision(
    db: Session,
    request_id: uuid.UUID,
    approval_role: ApprovalRole,
    decision: ApprovalDecision,
    decided_by: str,
    comments: str | None = None,
) -> PurchaseRequest:
    """
    Process a manager or finance approval decision.
    """

    if decision not in (
        ApprovalDecision.APPROVED,
        ApprovalDecision.REJECTED,
    ):
        raise ApprovalWorkflowError(
            "Decision must be APPROVED or REJECTED."
        )

    # Lock the purchase request while processing its decision.
    purchase_request = db.scalar(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request_id)
        .with_for_update()
    )

    if purchase_request is None:
        raise RequestNotFoundError("Purchase request not found.")

    if purchase_request.status != RequestStatus.PENDING:
        raise ApprovalWorkflowError(
            "This purchase request has already been processed."
        )

    # Find and lock the approval record for this role.
    approval = db.scalar(
        select(Approval)
        .where(
            Approval.request_id == request_id,
            Approval.approval_role == approval_role,
        )
        .with_for_update()
    )

    if approval is None:
        raise ApprovalNotFoundError(
            f"No {approval_role.value} approval exists for this request."
        )

    if approval.decision != ApprovalDecision.PENDING:
        raise ApprovalWorkflowError(
            "This approval has already been processed."
        )

    # Finance may only act after manager approval.
    if approval_role == ApprovalRole.FINANCE:
        manager_approval = db.scalar(
            select(Approval).where(
                Approval.request_id == request_id,
                Approval.approval_role == ApprovalRole.MANAGER,
            )
        )

        if (
            manager_approval is None
            or manager_approval.decision != ApprovalDecision.APPROVED
        ):
            raise ApprovalWorkflowError(
                "Finance cannot decide before manager approval."
            )

    # Record the decision.
    now = datetime.now(timezone.utc)

    approval.decision = decision
    approval.decided_by = decided_by
    approval.comments = comments
    approval.decided_at = now

    # Handle a rejected manager decision.
    if (
        approval_role == ApprovalRole.MANAGER
        and decision == ApprovalDecision.REJECTED
        and purchase_request.approval_route
        == ApprovalRoute.MANAGER_AND_FINANCE
    ):
        finance_approval = db.scalar(
            select(Approval)
            .where(
                Approval.request_id == request_id,
                Approval.approval_role == ApprovalRole.FINANCE,
            )
            .with_for_update()
        )

        if (
            finance_approval is not None
            and finance_approval.decision == ApprovalDecision.PENDING
        ):
            finance_approval.decision = ApprovalDecision.CANCELLED
            finance_approval.decided_by = "SYSTEM"
            finance_approval.comments = (
                "Cancelled because the manager rejected the request."
            )
            finance_approval.decided_at = now

    # Update the overall purchase request status.
    if decision == ApprovalDecision.REJECTED:
        purchase_request.status = RequestStatus.REJECTED

    elif approval_role == ApprovalRole.MANAGER:
        if purchase_request.approval_route == ApprovalRoute.MANAGER:
            purchase_request.status = RequestStatus.APPROVED

    elif approval_role == ApprovalRole.FINANCE:
        purchase_request.status = RequestStatus.APPROVED

    return purchase_request
