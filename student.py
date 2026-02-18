class Student:
    def __init__(self, student_id, name, age, grade, email, phone):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'email': self.email,
            'phone': self.phone
        }

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}"