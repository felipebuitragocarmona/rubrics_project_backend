# Academic Service API

Layered Flask service with Waitress, SQLite, repositories, services, controllers, and Bearer-token interceptor.

## Architecture

- `app/models`: entities and ORM mappings
- `app/repositories`: data access layer
- `app/services`: business rules
- `app/controllers`: REST presentation layer
- `app/middleware`: auth interceptor
- `app/utils`: security, serialization, db bootstrap
- `run.py`: Waitress entry point

## Auth interceptor

`app/middleware/auth_interceptor.py` validates the `Authorization: Bearer <token>` header.
Excluded endpoints:
- `POST /api/auth/login`
- `POST /api/auth/register-admin`
- `POST /api/users/public/register-student`
- `POST /api/users/public/register-teacher`
- `GET /health`

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Default seed user:
- email: `admin@example.com`
- password: `Admin123*`

## CRUD coverage

### Auth
- `POST /api/auth/login`
- `POST /api/auth/register-admin`

### Users
- `POST /api/users/`
- `GET /api/users/`
- `GET /api/users/<user_id>`
- `PUT /api/users/<user_id>`
- `DELETE /api/users/<user_id>`
- `PATCH /api/users/<user_id>/deactivate`
- `GET /api/users/search?...`

### Academic generic CRUD
Supported entities:
- `careers`
- `semesters`
- `subjects`
- `study-plans`
- `groups`
- `registrations`
- `enrollments`
- `students` (read/search/delete through generic endpoints)
- `teachers` (read/search/delete through generic endpoints)

Generic routes:
- `GET /api/academic/<entity_name>`
- `GET /api/academic/<entity_name>/<entity_id>`
- `PUT /api/academic/<entity_name>/<entity_id>`
- `DELETE /api/academic/<entity_name>/<entity_id>`
- `GET /api/academic/<entity_name>/search?<field>=<value>`

Specific create/actions:
- `POST /api/academic/careers`
- `POST /api/academic/semesters`
- `POST /api/academic/subjects`
- `POST /api/academic/study-plans`
- `POST /api/academic/groups`
- `PATCH /api/academic/groups/<group_id>/assign-teacher/<teacher_id>`
- `POST /api/academic/registrations`
- `POST /api/academic/enrollments`

### Evaluation generic CRUD
Supported entities:
- `rubrics`
- `criteria`
- `scales`
- `evaluations`
- `grades`
- `grade-details`

Generic routes:
- `GET /api/evaluation/<entity_name>`
- `GET /api/evaluation/<entity_name>/<entity_id>`
- `PUT /api/evaluation/<entity_name>/<entity_id>`
- `DELETE /api/evaluation/<entity_name>/<entity_id>`
- `GET /api/evaluation/<entity_name>/search?<field>=<value>`

Specific create/actions:
- `POST /api/evaluation/rubrics`
- `POST /api/evaluation/criteria`
- `POST /api/evaluation/scales`
- `PATCH /api/evaluation/rubrics/<rubric_id>/publish`
- `POST /api/evaluation/evaluations`
- `PATCH /api/evaluation/evaluations/<evaluation_id>/associate-rubric/<rubric_id>`
- `POST /api/evaluation/grades`
- `POST /api/evaluation/groups/<group_id>/register-final-scores`

## Design notes

- Only `1-1` and `1-n` relationships are used.
- `n-n` cases were resolved using bridge entities such as `Registration`, `Enrollment`, `StudyPlan`, and `GradeDetail`.
- Search is generic by query-string attribute name.
- Some business operations remain specialized even though the entities also expose generic CRUD routes.
