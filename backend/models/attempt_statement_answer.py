from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class AttemptStatementAnswer(Base):
    __tablename__ = "attempt_statement_answers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    attempt_answer_id: Mapped[int] = mapped_column(
        ForeignKey("attempt_answers.id"),
        nullable=False,
    )

    statement_id: Mapped[int] = mapped_column(
        ForeignKey("question_statements.id"),
        nullable=False,
    )

    selected_answer: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )