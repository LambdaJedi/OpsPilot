
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.purchase_request import PurchaseRequest
from backend.app.schemas.purchase_request import (
    PurchaseRequestCreate,
    PurchaseRequestResponse,
)
from backend.app.services.approval import determine_approval_route
from backend.app.services.approval_workflow import create_approval_records


router = APIRouter(
    prefix="/api/v1/requests",
    tags=["Purchase Requests"],
)


@router.post(
    "",
    response_model=PurchaseRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_purchase_request(
    request: PurchaseRequestCreate,
    db: Session = Depends(get_db),
):
    approval_route = determine_approval_route(request.amount)

    new_request = PurchaseRequest(
        requester_name=request.requester_name,
        department=request.department,
        title=request.title,
        description=request.description,
        amount=request.amount,
        currency=request.currency,
        approval_route=approval_route,
    )

    try:
        db.add(new_request)

        # Save the request within the current transaction
        # so that it receives its database ID.
        db.flush()

        # Create the required approval records.
        create_approval_records(db, new_request)

        # Save the request and approvals together.
        db.commit()

        db.refresh(new_request)

        return new_request

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create purchase request.",
        )


@router.get(
    "",
    response_model=list[PurchaseRequestResponse],
)
def list_purchase_requests(
    db: Session = Depends(get_db),
):
    statement = (
        select(PurchaseRequest)
        .order_by(PurchaseRequest.created_at.desc())
    )

    return db.scalars(statement).all()


@router.get(
    "/{request_id}",
    response_model=PurchaseRequestResponse,
)
def get_purchase_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    purchase_request = db.get(PurchaseRequest, request_id)

    if purchase_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase request not found.",
        )

    return purchase_request
