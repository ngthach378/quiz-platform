from sqlalchemy.orm import Session

from backend.models.attempt import Attempt
from backend.models.attempt_answer import AttemptAnswer
from backend.models.attempt_statement_answer import AttemptStatementAnswer
from backend.models.exam_question import ExamQuestion
from backend.models.numeric_answer import NumericAnswer
from backend.models.question import Question
from backend.models.question_statement import QuestionStatement


PART_I_SCORE = 0.25
PART_III_SCORE = 0.50

PART_II_SCORES = {
    0: 0.0,
    1: 0.10,
    2: 0.25,
    3: 0.50,
    4: 1.00,
}


def score_part_i(
    answer: AttemptAnswer,
    db: Session,
) -> float:
    if answer.selected_option_id is None:
        return 0.0

    from backend.models.question_option import QuestionOption

    option = (
        db.query(QuestionOption)
        .filter(QuestionOption.id == answer.selected_option_id)
        .first()
    )

    if option is None:
        return 0.0

    return PART_I_SCORE if option.is_correct else 0.0


def score_part_ii(
    answer: AttemptAnswer,
    db: Session,
) -> float:
    statements = (
        db.query(QuestionStatement)
        .filter(QuestionStatement.question_id == answer.question_id)
        .order_by(QuestionStatement.position)
        .all()
    )

    statement_answers = (
        db.query(AttemptStatementAnswer)
        .filter(
            AttemptStatementAnswer.attempt_answer_id == answer.id
        )
        .all()
    )

    selected_by_statement = {
        item.statement_id: item.selected_answer
        for item in statement_answers
    }

    correct_count = 0

    for statement in statements:
        selected_answer = selected_by_statement.get(statement.id)

        if selected_answer is not None:
            if selected_answer == statement.correct_answer:
                correct_count += 1

    return PART_II_SCORES[correct_count]


def score_part_iii(
    answer: AttemptAnswer,
    db: Session,
) -> float:
    if answer.numeric_answer is None:
        return 0.0

    try:
        student_value = float(answer.numeric_answer)
    except (TypeError, ValueError):
        return 0.0

    numeric_answer = (
        db.query(NumericAnswer)
        .filter(NumericAnswer.question_id == answer.question_id)
        .first()
    )

    if numeric_answer is None:
        return 0.0

    if (
        abs(student_value - numeric_answer.correct_value)
        <= numeric_answer.tolerance
    ):
        return PART_III_SCORE

    return 0.0


def calculate_attempt_score(
    attempt: Attempt,
    db: Session,
) -> float:
    answers = (
        db.query(AttemptAnswer)
        .filter(AttemptAnswer.attempt_id == attempt.id)
        .all()
    )

    total_score = 0.0

    for answer in answers:
        exam_question = (
            db.query(ExamQuestion)
            .filter(
                ExamQuestion.exam_id == attempt.exam_id,
                ExamQuestion.question_id == answer.question_id,
            )
            .first()
        )

        if exam_question is None:
            continue

        question = (
            db.query(Question)
            .filter(Question.id == answer.question_id)
            .first()
        )

        if question is None:
            continue

        if exam_question.part == 1:
            score = score_part_i(answer, db)

        elif exam_question.part == 2:
            score = score_part_ii(answer, db)

        elif exam_question.part == 3:
            score = score_part_iii(answer, db)

        else:
            score = 0.0

        answer.is_correct = score > 0
        total_score += score

    return round(total_score, 2)