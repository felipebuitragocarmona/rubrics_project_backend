from app import create_app
from app.models import db
from app.models.entities import User, Teacher, Student, Career, Subject, StudyPlan, Group, Registration, Enrollment
from app.utils.security import hash_password

app = create_app()

with app.app_context():
    db.create_all()

    # Users
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(email='admin@example.com', password_hash=hash_password('Admin123*'), code='ADM-001', role='ADMIN', is_active=True)
        db.session.add(admin)

    # Career
    career = Career.query.filter_by(code='ENG-001').first()
    if not career:
        career = Career(name='Engineering', code='ENG-001', description='Engineering career')
        db.session.add(career)

    # Subjects
    math = Subject.query.filter_by(code='MATH-101').first()
    if not math:
        math = Subject(name='Mathematics I', code='MATH-101', credits=3)
        db.session.add(math)

    physics = Subject.query.filter_by(code='PHYS-101').first()
    if not physics:
        physics = Subject(name='Physics I', code='PHYS-101', credits=3)
        db.session.add(physics)

    db.session.commit()

    # Study Plan
    sp = StudyPlan.query.filter_by(name='Plan 2026').first()
    if not sp:
        sp = StudyPlan(career_id=career.id, name='Plan 2026', year=2026, suggested_semester=1, is_published=False)
        db.session.add(sp)
        db.session.commit()
        # link subjects
        sp.subjects.append(math)
        sp.subjects.append(physics)

    # Teacher & Student
    teacher_user = User.query.filter_by(email='teacher@example.com').first()
    if not teacher_user:
        teacher_user = User(email='teacher@example.com', password_hash=hash_password('Teacher123'), code='TCH-001', role='TEACHER')
        db.session.add(teacher_user)
        db.session.commit()
        teacher = Teacher(user_id=teacher_user.id, first_name='Toni', last_name='Docente', identification='TCH123')
        db.session.add(teacher)

    student_user = User.query.filter_by(email='student@example.com').first()
    if not student_user:
        student_user = User(email='student@example.com', password_hash=hash_password('Student123'), code='STU-001', role='STUDENT')
        db.session.add(student_user)
        db.session.commit()
        student = Student(user_id=student_user.id, first_name='Ana', last_name='Alumno', identification='STU123')
        db.session.add(student)

    db.session.commit()

    # Registration and Enrollment example
    student = Student.query.filter_by(identification='STU123').first()
    if student and not Registration.query.filter_by(student_id=student.id, career_id=career.id).first():
        reg = Registration(career_id=career.id, student_id=student.id, admission_period='2026-01', academic_status='ACTIVE')
        db.session.add(reg)
        db.session.commit()

    print('Seeding complete')
