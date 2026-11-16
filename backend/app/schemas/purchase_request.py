
import uuid

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.purchase_request import (
    ApprovalRoute,
    RequestStatus,
)


class PurchaseRequestCreate(BaseModel):
    requester_name: str = Field(min_length=2, max_length=120)
    department: str = Field(min_length=2, max_length=100)
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="ZAR", pattern=r"^[A-Z]{3}$")


class PurchaseRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    requester_name: str
    department: str
    title: str
    description: str
    amount: Decimal
    currency: str
    approval_route: ApprovalRoute
    status: RequestStatus
    created_at: datetime
