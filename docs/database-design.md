# Quiz Platform — Database Design

## 1. Overview

Hệ thống phục vụ thi và luyện tập môn Toán theo cấu trúc đề thi THPTQG 2026.

Bài thi gồm 3 phần:

- Phần I: 12 câu trắc nghiệm 4 đáp án.
- Phần II: 4 câu trắc nghiệm Đúng/Sai, mỗi câu 4 ý.
- Phần III: 6 câu trả lời ngắn dạng số.

Tổng điểm tối đa: 10 điểm.

## 2. Scoring Rules

### Part I

- 12 câu.
- Mỗi câu có 4 lựa chọn.
- Chỉ có 1 đáp án đúng.
- Đúng: 0.25 điểm.
- Sai: 0 điểm.

### Part II

Mỗi câu có 4 ý Đúng/Sai.

| Số ý đúng | Điểm |
|-----------|------|
| 1 | 0.10 |
| 2 | 0.25 |
| 3 | 0.50 |
| 4 | 1.00 |

### Part III

- 6 câu.
- Thí sinh nhập đáp án dạng số.
- Mỗi câu đúng: 0.50 điểm.

## 3. Entities

### Users

- id
- username
- email

### Exams

- id
- title
- year
- subject
- description
- is_published
- created_at
- updated_at

### Questions

- id
- content
- question_type
- explanation
- difficulty
- created_at
- updated_at

Question types:

- MCQ
- TRUE_FALSE
- NUMERIC

### Exam Questions

- id
- exam_id
- question_id
- part
- question_number

### Question Options

- id
- question_id
- option_label
- content
- position
- is_correct

### Question Statements

- id
- question_id
- content
- position
- correct_answer

### Numeric Answers

- id
- question_id
- correct_value
- tolerance

### Attempts

- id
- user_id
- exam_id
- started_at
- submitted_at
- score
- status

### Attempt Answers

- id
- attempt_id
- question_id
- selected_option_id
- numeric_answer
- is_correct

### Attempt Statement Answers

- id
- attempt_answer_id
- statement_id
- selected_answer

## 4. Scoring Engine

Điểm được tính dựa trên câu trả lời của thí sinh.

### Part I

Đúng = 0.25 điểm.

### Part II

- 1 ý đúng = 0.10 điểm
- 2 ý đúng = 0.25 điểm
- 3 ý đúng = 0.50 điểm
- 4 ý đúng = 1.00 điểm

### Part III

Nếu:

abs(student_answer - correct_value) <= tolerance

thì được 0.50 điểm.

## 5. Design Principles

- Question không chứa score cố định.
- ExamQuestion xác định câu hỏi thuộc đề nào, phần nào và vị trí nào.
- Part II sử dụng Question Statements.
- Part III sử dụng Numeric Answer.
- Attempt lưu một lần làm bài của người dùng.

## 6. Initial Database Tables

1. users
2. exams
3. questions
4. exam_questions
5. question_options
6. question_statements
7. numeric_answers
8. attempts
9. attempt_answers
10. attempt_statement_answers
