from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Instructor, Course, Student, Enrollment
from alembic import command
from alembic.config import Config

DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_U_nGI5N9gKIDfCh1wrY@mysqlbds-lbsbds.f.aivencloud.com:27913/defaultdb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def display_table_data():
    while True:
        print("\nМеню:")
        print("1. Вивести всі таблиці")
        print("2. Вивести категорії")
        print("3. Вивести інструкторів")
        print("4. Вивести курси")
        print("5. Вивести студентів")
        print("6. Вивести запис на курси")
        print("0. Вихід")
        
        choice = input("Оберіть опцію: ")
        
        if choice == "1":
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

        elif choice == "2":
            categories = session.query(Category).all()
            for category in categories:
                print(f"ID: {category.category_id}, Name: {category.name}, Description: {category.description}")
        elif choice == "3":
            instructors = session.query(Instructor).all()
            for instructor in instructors:
                print(f"ID: {instructor.instructor_id}, Name: {instructor.first_name} {instructor.last_name}, Email: {instructor.email}")
        elif choice == "4":
            courses = session.query(Course).all()
            for course in courses:
                print(f"ID: {course.course_id}, Title: {course.title}, Description: {course.description}, Category ID: {course.category_id}, Instructor ID: {course.instructor_id}")
        elif choice == "5":
            students = session.query(Student).all()
            for student in students:
                print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, Email: {student.email}")
        elif choice == "6":
            enrollments = session.query(Enrollment).all()
            for enrollment in enrollments:
                print(f"Enrollment ID: {enrollment.enrollment_id}, Student ID: {enrollment.student_id}, Course ID: {enrollment.course_id}, Enrollment Date: {enrollment.enrollment_date}, Progress: {enrollment.progress_percentage}%")
        elif choice == "0":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    display_table_data()
