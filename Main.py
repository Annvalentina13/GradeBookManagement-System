import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GradebookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Professional Gradebook Management System")
        self.geometry("950x700")
        self.configure(bg="#f0f4f8")  # Light neutral background

        # Data storage dictionaries
        self.students = {}
        self.subjects = {}
        self.grades = defaultdict(dict)  # {student_id: {subject_code: marks}}

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure_styles()

        self.create_widgets()

    def configure_styles(self):
        self.style.configure('TFrame', background="#f0f4f8")
        self.style.configure('TLabel', background="#f0f4f8", font=("Segoe UI", 11))
        self.style.configure('TButton', font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map('TButton', background=[('active', '#4a69ad')], foreground=[('active', 'white')])

    def create_widgets(self):
        # Sidebar navigation
        sidebar = ttk.Frame(self, width=200, relief='raised')
        sidebar.pack(side='left', fill='y', padx=2, pady=2)

        ttk.Button(sidebar, text="Students", command=self.show_students).pack(fill='x', pady=10, padx=10)
        ttk.Button(sidebar, text="Subjects", command=self.show_subjects).pack(fill='x', pady=10, padx=10)
        ttk.Button(sidebar, text="Grades", command=self.show_grades).pack(fill='x', pady=10, padx=10)
        ttk.Button(sidebar, text="Analytics", command=self.show_analytics).pack(fill='x', pady=10, padx=10)

        # Main container for pages
        self.container = ttk.Frame(self)
        self.container.pack(side='right', fill='both', expand=True)

        # Create and grid pages
        self.pages = {}
        for Page in (StudentsPage, SubjectsPage, GradesPage, AnalyticsPage):
            page = Page(self.container, self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky='nsew')

        self.show_students()

    def show_students(self):
        self.pages[StudentsPage].update_table()
        self.pages[StudentsPage].tkraise()

    def show_subjects(self):
        self.pages[SubjectsPage].update_table()
        self.pages[SubjectsPage].tkraise()

    def show_grades(self):
        self.pages[GradesPage].update_form()
        self.pages[GradesPage].tkraise()

    def show_analytics(self):
        self.pages[AnalyticsPage].update_chart()
        self.pages[AnalyticsPage].tkraise()

# Students Page
class StudentsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text='Students', font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.controller = controller

        columns = ("ID", "Name", "Email")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text='Add Student', command=self.add_student).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Edit Student', command=self.edit_student).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Delete Student', command=self.delete_student).pack(side='left', padx=5)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for sid, info in self.controller.students.items():
            self.tree.insert('', 'end', values=(sid, info['name'], info['email']))

    def add_student(self):
        self.open_student_form()

    def edit_student(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            self.open_student_form(values)
        else:
            messagebox.showwarning("Select Student", "Please select a student to edit.")

    def delete_student(self):
        selected = self.tree.selection()
        if selected:
            sid = self.tree.item(selected[0], 'values')[0]
            self.controller.students.pop(sid, None)
            self.controller.grades.pop(sid, None)  # Remove grades too
            self.update_table()
        else:
            messagebox.showwarning("Select Student", "Please select a student to delete.")

    def open_student_form(self, values=None):
        form = tk.Toplevel(self)
        form.title("Student Form")
        form.geometry("300x200")
        labels = ['ID', 'Name', 'Email']
        entries = {}

        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, padx=10, pady=10)
            entry = ttk.Entry(form)
            entry.grid(row=i, column=1, padx=10, pady=10)
            if values:
                entry.insert(0, values[i])
            entries[label.lower()] = entry

        def save():
            sid = entries['id'].get().strip()
            name = entries['name'].get().strip()
            email = entries['email'].get().strip()
            if not sid or not name:
                messagebox.showerror("Error", "Student ID and Name required.")
                return
            if sid in self.controller.students and not values:
                messagebox.showerror("Error", "Student ID already exists.")
                return
            self.controller.students[sid] = {'name': name, 'email': email}
            self.update_table()
            form.destroy()

        ttk.Button(form, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=10)

# Subjects Page
class SubjectsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text='Subjects', font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.controller = controller

        self.tree = ttk.Treeview(self, columns=("Code", "Name"), show='headings')
        self.tree.heading("Code", text="Subject Code")
        self.tree.heading("Name", text="Subject Name")
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text='Add Subject', command=self.add_subject).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Edit Subject', command=self.edit_subject).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Delete Subject', command=self.delete_subject).pack(side='left', padx=5)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for code, name in self.controller.subjects.items():
            self.tree.insert('', 'end', values=(code, name))

    def add_subject(self):
        self.open_subject_form()

    def edit_subject(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            self.open_subject_form(values)
        else:
            messagebox.showwarning("Select Subject", "Please select a subject to edit.")

    def delete_subject(self):
        selected = self.tree.selection()
        if selected:
            code = self.tree.item(selected[0], 'values')[0]
            self.controller.subjects.pop(code, None)
            # Remove related grades
            for sid in list(self.controller.grades.keys()):
                if code in self.controller.grades[sid]:
                    del self.controller.grades[sid][code]
            self.update_table()
        else:
            messagebox.showwarning("Select Subject", "Please select a subject to delete.")

    def open_subject_form(self, values=None):
        form = tk.Toplevel(self)
        form.title("Subject Form")
        form.geometry("300x150")
        ttk.Label(form, text='Subject Code:').grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(form, text='Subject Name:').grid(row=1, column=0, padx=10, pady=10)

        code_entry = ttk.Entry(form)
        name_entry = ttk.Entry(form)
        code_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        if values:
            code_entry.insert(0, values[0])
            name_entry.insert(0, values[1])

        def save():
            code, name = code_entry.get().strip(), name_entry.get().strip()
            if not code or not name:
                messagebox.showerror("Error", "Subject code and name required.")
                return
            if code in self.controller.subjects and not values:
                messagebox.showerror("Error", "Subject code already exists.")
                return
            self.controller.subjects[code] = name
            self.update_table()
            form.destroy()

        ttk.Button(form, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)

# Grades Page
class GradesPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text='Grades', font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.controller = controller

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Student:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Subject:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Marks:").grid(row=2, column=0, padx=5, pady=5)

        self.student_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.marks_var = tk.StringVar()

        self.student_cb = ttk.Combobox(form_frame, textvariable=self.student_var)
        self.subject_cb = ttk.Combobox(form_frame, textvariable=self.subject_var)
        ttk.Entry(form_frame, textvariable=self.marks_var).grid(row=2, column=1, padx=5, pady=5)

        self.student_cb.grid(row=0, column=1, padx=5, pady=5)
        self.subject_cb.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self, text="Add/Update Grade", command=self.add_update_grade).pack(pady=5)
        ttk.Button(self, text="Calculate GPA", command=self.calculate_gpa).pack(pady=5)

        self.gpa_label = ttk.Label(self, text="GPA: N/A", font=("Segoe UI", 12, "bold"))
        self.gpa_label.pack(pady=10)

    def update_form(self):
        self.student_cb['values'] = list(self.controller.students.keys())
        self.subject_cb['values'] = list(self.controller.subjects.keys())

    def add_update_grade(self):
        sid = self.student_var.get()
        sub_code = self.subject_var.get()
        try:
            marks = float(self.marks_var.get())
            if not (0 <= marks <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid marks (0-100).")
            return

        if sid not in self.controller.students:
            messagebox.showerror("Error", "Selected student does not exist.")
            return
        if sub_code not in self.controller.subjects:
            messagebox.showerror("Error", "Selected subject does not exist.")
            return

        self.controller.grades[sid][sub_code] = marks
        messagebox.showinfo("Success", f"Grade recorded: {marks} for {sid} in {sub_code}.")

    def calculate_gpa(self):
        sid = self.student_var.get()
        student_grades = self.controller.grades.get(sid, {})
        if student_grades:
            gpa = sum(student_grades.values()) / len(student_grades)
            self.gpa_label.config(text=f"GPA: {gpa:.2f}")
        else:
            self.gpa_label.config(text="GPA: N/A")

# Analytics Page
class AnalyticsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text='Analytics', font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill='both', expand=True)

        self.figure = plt.Figure(figsize=(8,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def update_chart(self):
        self.ax.clear()
        subject_totals = defaultdict(float)
        subject_counts = defaultdict(int)

        for grades in self.controller.grades.values():
            for subj, mark in grades.items():
                subject_totals[subj] += mark
                subject_counts[subj] += 1

        subjects = list(subject_totals.keys())
        averages = [(subject_totals[subj]/subject_counts[subj]) if subject_counts[subj] else 0 for subj in subjects]

        if subjects:
            self.ax.bar(subjects, averages, color='cornflowerblue')
            self.ax.set_title("Average Grades per Subject")
            self.ax.set_ylabel("Average Mark")
            self.ax.set_ylim(0, 100)
            self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        else:
            self.ax.text(0.5, 0.5, 'No grade data available',
                         horizontalalignment='center', verticalalignment='center',
                         transform=self.ax.transAxes, fontsize=14)

        self.canvas.draw()

if __name__ == "__main__":
    app = GradebookApp()
    app.mainloop()
