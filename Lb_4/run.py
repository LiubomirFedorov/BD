from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, lazyload, joinedload, subqueryload
from models import Category, Instructor, Course, Student, Enrollment
from alembic import command
from alembic.config import Config

DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_U_nGI5N9gKIDfCh1wrY@mysqlbds-lbsbds.f.aivencloud.com:27913/defaultdb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def display_table_data():
    categories = session.query(Category).all()
    instructors = session.query(Instructor).all()
    courses = session.query(Course).all()
    students = session.query(Student).all()
    enrollments = session.query(Enrollment).all()

    print("\nКатегорії:")
    for category in categories:
        print(f"ID: {category.category_id}, Name: {category.name}, Description: {category.description}")
    
    print("\nІнструктори:")
    for instructor in instructors:
        print(f"ID: {instructor.instructor_id}, Name: {instructor.first_name} {instructor.last_name}, Email: {instructor.email}")
    
    print("\nКурси:")
    for course in courses:
        print(f"ID: {course.course_id}, Title: {course.title}, Description: {course.description}, Category ID: {course.category_id}, Instructor ID: {course.instructor_id}")
    
    print("\nСтуденти:")
    for student in students:
        print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, Email: {student.email}")
    
    print("\nЗапис на курси:")
    for enrollment in enrollments:
        print(f"Enrollment ID: {enrollment.enrollment_id}, Student ID: {enrollment.student_id}, Course ID: {enrollment.course_id}, Enrollment Date: {enrollment.enrollment_date}, Progress: {enrollment.progress_percentage}%")

def create_record():
    # Створення нового запису
    new_category = Category(name="Новий курс", description="Опис нового курсу")
    session.add(new_category)
    session.commit()
    print("Запис додано в таблицю 'Категорії'.")

def delete_record():
    # Видалення запису
    category_to_delete = session.query(Category).filter_by(name="Новий курс").first()
    if category_to_delete:
        session.delete(category_to_delete)
        session.commit()
        print(f"Запис з категорією '{category_to_delete.name}' видалено.")
    else:
        print("Запис не знайдено для видалення.")

def cascade_delete():
    # Каскадне видалення: видалення категорії, яка має курси та записи на курси
    category_to_cascade_delete = session.query(Category).filter_by(name="Marketing").first()
    if category_to_cascade_delete:
        # Каскадне видалення записів на курси
        for course in category_to_cascade_delete.courses:
            for enrollment in course.enrollments:
                session.delete(enrollment)
            session.delete(course)
        session.delete(category_to_cascade_delete)
        session.commit()
        print(f"Каскадне видалення для категорії '{category_to_cascade_delete.name}' успішно виконано.")
    else:
        print("Категорія не знайдена для каскадного видалення.")

def update_record():
    # Внесення змін у запис
    category_to_update = session.query(Category).filter_by(name="Design").first()
    if category_to_update:
        category_to_update.name = "Design"
        category_to_update.description = "Оновлений опис курсу"
        session.commit()
        print(f"Запис категорії '{category_to_update.name}' оновлено.")
    else:
        print("Категорія для оновлення не знайдена.")

def lazy_loading(session):
    print("Категорії (Lazy Loading):")
    categories = session.query(Category).all()  # Base query to load categories
    for category in categories:
        # Lazy loading courses for each category (when accessed)
        print(f"ID: {category.category_id}, Name: {category.name}, Description: {category.description}")
        for course in category.courses:
            print(f"  - Course ID: {course.course_id}, Title: {course.title}")
    print()

def eager_loading(session):
    print("Курси з категоріями та інструкторами (Eager Loading):")
    courses = session.query(Course).options(joinedload(Course.category), joinedload(Course.instructor)).all()
    for course in courses:
        print(f"ID: {course.course_id}, Title: {course.title}, Description: {course.description}")
        print(f"  Category: {course.category.name}, Instructor: {course.instructor.first_name} {course.instructor.last_name}")
    print()

def explicit_loading(session):
    print("Студенти та їх записи на курси (Explicit Loading):")
    students = session.query(Student).all()
    for student in students:
        # Explicit loading of enrollments for each student
        enrollments = session.query(Enrollment).filter(Enrollment.student_id == student.student_id).all()
        print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}")
        for enrollment in enrollments:
            print(f"  - Course ID: {enrollment.course_id}, Enrollment Date: {enrollment.enrollment_date}")
    print()

def filter_data(session):
    print("Фільтрація та сортування даних за прогресом студентів:")
    students = session.query(Student).join(Enrollment).filter(Enrollment.progress_percentage > 80).order_by(Enrollment.progress_percentage.desc()).all()
    for student in students:
        print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, Progress: {student.enrollments[0].progress_percentage}%")
    print()

def main_menu():
    while True:
        print("\nМеню:")
        print("1. Вивести всі таблиці")
        print("2. Створити новий запис")
        print("3. Видалити запис")
        print("4. Каскадне видалення")
        print("5. Оновити запис")
        print("6. Lazy Loading")
        print("7. Eager Loading")
        print("8. Explicit Loading")
        print("9. Фільтрація та сортування")
        print("0. Вихід")
        
        choice = input("Оберіть опцію: ")
        
        if choice == "1":
            display_table_data()
        elif choice == "2":
            create_record()
            display_table_data()
        elif choice == "3":
            delete_record()
            display_table_data()
        elif choice == "4":
            cascade_delete()
            display_table_data()
        elif choice == "5":
            update_record()
            display_table_data()
        elif choice == "6":
            lazy_loading(session)
        elif choice == "7":
            eager_loading(session)
        elif choice == "8":
            explicit_loading(session)
        elif choice == "9":
            filter_data(session)
        elif choice == "0":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main_menu()