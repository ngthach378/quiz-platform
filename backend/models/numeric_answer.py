from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class NumericAnswer(Base):
    __tablename__ = "numeric_answers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
        nullable=False,
    )

    correct_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    tolerance: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
