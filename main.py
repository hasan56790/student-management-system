import tkinter as tk
from gui import StudentManagementGUI

def main():
    """Main function to run the Student Management System"""
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()