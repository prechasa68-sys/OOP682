from models.person import Person
from models.student import Student  
from models.staff import Staff




def get_person_info(person: Person):
    print(isinstance(person, Person))
    return f"ID: {person.pid}, Name: {person.name}, Age: {person.age}"



if __name__ == "__main__" :
    # Define person, student, staff objects
    person = Person(1234567890123, "John Doe", 30)
    student = Student(1234567890123, "Alice", 20, "S123")
    staff = Staff(2345678901234, "Bob", 35, "ST678")

    # Print specific info for student and staff (using their specific attributes)
    print(f"Student: {student.name}, Age: {student.age}, Student ID: {student.student_id}")
    print(f"Staff: {staff.name}, Age: {staff.age}, Staff ID: {staff.staff_id}")

    # Call get_person_info for each object and print its returned value
    print(get_person_info(person))
    print(get_person_info(student))
    print(get_person_info(staff))