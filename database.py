import sqlite3
from student import Student


class Database:
    def __init__(self, db_name="students.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create students table if it doesn't exist"""
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS students
                            (
                                student_id
                                TEXT
                                PRIMARY
                                KEY,
                                name
                                TEXT
                                NOT
                                NULL,
                                age
                                INTEGER,
                                grade
                                TEXT,
                                email
                                TEXT,
                                phone
                                TEXT
                            )
                            ''')
        self.conn.commit()

    def add_student(self, student):
        """Add a new student to database"""
        try:
            self.cursor.execute('''
                                INSERT INTO students (student_id, name, age, grade, email, phone)
                                VALUES (?, ?, ?, ?, ?, ?)
                                ''', (student.student_id, student.name, student.age,
                                      student.grade, student.email, student.phone))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Student ID already exists

    def get_all_students(self):
        """Retrieve all students"""
        self.cursor.execute('SELECT * FROM students ORDER BY name')
        rows = self.cursor.fetchall()
        students = []
        for row in rows:
            student = Student(row[0], row[1], row[2], row[3], row[4], row[5])
            students.append(student)
        return students

    def search_student(self, search_term):
        """Search students by ID or name"""
        self.cursor.execute('''
                            SELECT *
                            FROM students
                            WHERE student_id LIKE ?
                               OR name LIKE ?
                            ORDER BY name
                            ''', (f'%{search_term}%', f'%{search_term}%'))
        rows = self.cursor.fetchall()
        students = []
        for row in rows:
            student = Student(row[0], row[1], row[2], row[3], row[4], row[5])
            students.append(student)
        return students

    def update_student(self, student_id, **kwargs):
        """Update student information"""
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)

        if fields:
            query = f"UPDATE students SET {', '.join(fields)} WHERE student_id = ?"
            values.append(student_id)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        return False

    def delete_student(self, student_id):
        """Delete a student by ID"""
        self.cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_student_count(self):
        """Get total number of students"""
        self.cursor.execute('SELECT COUNT(*) FROM students')
        return self.cursor.fetchone()[0]

    def close(self):
        """Close database connection"""
        self.conn.close()