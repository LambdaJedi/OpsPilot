
import enum
import uuid

from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base


class ApprovalRole(str, enum.Enum):
    MANAGER = "MANAGER"
    FINANCE = "FINANCE"


class ApprovalDecision(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class Approval(Base):
    __tablename__ = "approvals"

    __table_args__ = (
        UniqueConstraint(
            "request_id",
            "approval_role",
            name="uq_approval_request_role",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("purchase_requests.id", ondelete="CASCADE"),
        nullable=False,
    )

    approval_role: Mapped[ApprovalRole] = mapped_column(
        Enum(ApprovalRole, name="approval_role"),
        nullable=False,
    )

    decision: Mapped[ApprovalDecision] = mapped_column(
        Enum(ApprovalDecision, name="approval_decision"),
        default=ApprovalDecision.PENDING,
        nullable=False,
    )

    decided_by: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    comments: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    decided_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
