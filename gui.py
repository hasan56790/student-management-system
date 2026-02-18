import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database
from student import Student
from datetime import datetime


class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        # Initialize database
        self.db = Database()

        # Set style
        self.setup_styles()

        # Create GUI elements
        self.create_menu()
        self.create_widgets()
        self.refresh_table()

        # Bind keyboard shortcuts
        self.root.bind('<Control-f>', lambda e: self.search_students())
        self.root.bind('<Control-n>', lambda e: self.add_student())
        self.root.bind('<Delete>', lambda e: self.delete_student())

    def setup_styles(self):
        """Configure styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        self.bg_color = '#f0f0f0'
        self.header_color = '#2c3e50'
        self.button_color = '#3498db'
        self.root.configure(bg=self.bg_color)

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Add Student", command=self.add_student)
        edit_menu.add_command(label="Edit Student", command=self.edit_student)
        edit_menu.add_command(label="Delete Student", command=self.delete_student)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_table)
        view_menu.add_command(label="Statistics", command=self.show_statistics)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        """Create main GUI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.header_color, height=60)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(header_frame, text="Student Management System",
                               font=('Arial', 20, 'bold'),
                               bg=self.header_color, fg='white')
        title_label.pack(pady=15)

        # Search frame
        search_frame = tk.Frame(self.root, bg=self.bg_color)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Search:", bg=self.bg_color,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_students())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                width=40, font=('Arial', 10))
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.focus()

        # Button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Buttons
        buttons = [
            ("Add Student", self.add_student, '#27ae60'),
            ("Edit Student", self.edit_student, '#f39c12'),
            ("Delete Student", self.delete_student, '#e74c3c'),
            ("Refresh", self.refresh_table, '#3498db'),
            ("Statistics", self.show_statistics, '#9b59b6')
        ]

        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                            bg=color, fg='white', font=('Arial', 10, 'bold'),
                            padx=15, pady=5, relief=tk.FLAT)
            btn.pack(side=tk.LEFT, padx=5)

        # Treeview frame
        tree_frame = tk.Frame(self.root, bg=self.bg_color)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        self.tree = ttk.Treeview(tree_frame,
                                 columns=('ID', 'Name', 'Age', 'Grade', 'Email', 'Phone'),
                                 show='tree headings',
                                 yscrollcommand=v_scrollbar.set,
                                 xscrollcommand=h_scrollbar.set)

        # Configure columns
        self.tree.heading('#0', text='')
        self.tree.heading('ID', text='Student ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Grade', text='Grade')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Phone', text='Phone')

        self.tree.column('#0', width=0, stretch=False)
        self.tree.column('ID', width=100)
        self.tree.column('Name', width=200)
        self.tree.column('Age', width=50)
        self.tree.column('Grade', width=100)
        self.tree.column('Email', width=200)
        self.tree.column('Phone', width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)

        # Bind double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_student())

        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W, bg='#ecf0f1')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def refresh_table(self):
        """Refresh the student table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all students and insert
        students = self.db.get_all_students()
        for student in students:
            self.tree.insert('', 'end', values=(
                student.student_id,
                student.name,
                student.age,
                student.grade,
                student.email,
                student.phone
            ))

        # Update status bar
        count = self.db.get_student_count()
        self.status_bar.config(text=f"Total Students: {count}")

    def search_students(self):
        """Search students based on search term"""
        search_term = self.search_var.get().strip()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Search and display results
        if search_term:
            students = self.db.search_student(search_term)
            result_text = f"Search results for '{search_term}': {len(students)} found"
        else:
            students = self.db.get_all_students()
            result_text = f"Total Students: {len(students)}"

        for student in students:
            self.tree.insert('', 'end', values=(
                student.student_id,
                student.name,
                student.age,
                student.grade,
                student.email,
                student.phone
            ))

        self.status_bar.config(text=result_text)

    def add_student(self):
        """Open dialog to add new student"""
        dialog = StudentDialog(self.root, "Add New Student")
        if dialog.result:
            student = Student(
                dialog.result['student_id'],
                dialog.result['name'],
                dialog.result['age'],
                dialog.result['grade'],
                dialog.result['email'],
                dialog.result['phone']
            )

            if self.db.add_student(student):
                messagebox.showinfo("Success", "Student added successfully!")
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Student ID already exists!")

    def edit_student(self):
        """Edit selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return

        # Get current values
        values = self.tree.item(selected[0])['values']

        dialog = StudentDialog(self.root, "Edit Student", values)
        if dialog.result:
            student_id = values[0]  # Original ID
            self.db.update_student(
                student_id,
                name=dialog.result['name'],
                age=dialog.result['age'],
                grade=dialog.result['grade'],
                email=dialog.result['email'],
                phone=dialog.result['phone']
            )
            messagebox.showinfo("Success", "Student updated successfully!")
            self.refresh_table()

    def delete_student(self):
        """Delete selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete.")
            return

        values = self.tree.item(selected[0])['values']

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete {values[1]}?"):
            if self.db.delete_student(values[0]):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Failed to delete student.")

    def show_statistics(self):
        """Show statistics dialog"""
        count = self.db.get_student_count()
        students = self.db.get_all_students()

        # Calculate average age
        if students:
            avg_age = sum(s.age for s in students if s.age) / len(students)
            avg_age = f"{avg_age:.1f}"
        else:
            avg_age = "N/A"

        # Grade distribution
        grades = {}
        for student in students:
            if student.grade:
                grades[student.grade] = grades.get(student.grade, 0) + 1

        stats_text = f"Total Students: {count}\n"
        stats_text += f"Average Age: {avg_age}\n\n"
        stats_text += "Grade Distribution:\n"
        for grade, count in grades.items():
            stats_text += f"  {grade}: {count} students\n"

        messagebox.showinfo("Statistics", stats_text)

    def export_to_csv(self):
        """Export student data to CSV file"""
        import csv
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            students = self.db.get_all_students()

            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Student ID', 'Name', 'Age', 'Grade', 'Email', 'Phone'])

                for student in students:
                    writer.writerow([
                        student.student_id,
                        student.name,
                        student.age,
                        student.grade,
                        student.email,
                        student.phone
                    ])

            messagebox.showinfo("Success", f"Data exported to {filename}")

    def show_about(self):
        """Show about dialog"""
        about_text = """Student Management System
Version 1.0

A comprehensive system for managing student records.
Created with Python and Tkinter.

Features:
- Add, edit, and delete student records
- Search functionality
- Export to CSV
- Statistics
- User-friendly interface"""

        messagebox.showinfo("About", about_text)

    def __del__(self):
        """Clean up database connection"""
        if hasattr(self, 'db'):
            self.db.close()


class StudentDialog:
    """Dialog for adding/editing students"""

    def __init__(self, parent, title, values=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (350 // 2)
        self.dialog.geometry(f"+{x}+{y}")

        # Create form
        self.create_form(values)

        # Bind Enter key to submit
        self.dialog.bind('<Return>', lambda e: self.submit())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())

        self.dialog.wait_window()

    def create_form(self, values):
        """Create input form"""
        # Main frame
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Form fields
        fields = [
            ('Student ID:', 'student_id'),
            ('Name:', 'name'),
            ('Age:', 'age'),
            ('Grade:', 'grade'),
            ('Email:', 'email'),
            ('Phone:', 'phone')
        ]

        self.entries = {}

        for i, (label, field) in enumerate(fields):
            tk.Label(main_frame, text=label, font=('Arial', 10)).grid(
                row=i, column=0, sticky='w', pady=5)

            entry = tk.Entry(main_frame, font=('Arial', 10), width=30)
            entry.grid(row=i, column=1, pady=5, padx=(10, 0))

            # Set initial values if editing
            if values and i < len(values):
                entry.insert(0, values[i])

            self.entries[field] = entry

        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Submit", command=self.submit,
                  bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                  padx=20, pady=5).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy,
                  bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                  padx=20, pady=5).pack(side=tk.LEFT, padx=5)

    def submit(self):
        """Validate and submit form"""
        # Get values
        result = {}
        for field, entry in self.entries.items():
            value = entry.get().strip()
            if not value:
                messagebox.showwarning("Warning", f"{field.replace('_', ' ').title()} is required!")
                entry.focus()
                return
            result[field] = value

        # Validate age
        try:
            if result['age']:
                age = int(result['age'])
                if age < 0 or age > 150:
                    messagebox.showwarning("Warning", "Please enter a valid age (0-150)")
                    self.entries['age'].focus()
                    return
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number for age")
            self.entries['age'].focus()
            return

        # Validate email format (basic)
        if '@' not in result['email'] or '.' not in result['email']:
            messagebox.showwarning("Warning", "Please enter a valid email address")
            self.entries['email'].focus()
            return

        self.result = result
        self.dialog.destroy()