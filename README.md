# 📘 Gradebook Management System (Tkinter)

A **Professional Desktop Application** built using **Python’s Tkinter library**, designed for teachers and administrators to efficiently manage **students, subjects, grades, and analytics** — all within a clean and modern user interface.

---

## 🖥️ Features

### 🧭 Dashboard & Navigation
- Sidebar-based navigation with clean layout  
- Organized pages for **Students**, **Subjects**, **Grades**, and **Analytics**  
- Consistent theme using modern neutral tones (`#f0f4f8`, `cornflowerblue`)  

### 👩‍🎓 Students Management
- Add, edit, or delete student records  
- Display all students in a table with columns: **ID**, **Name**, and **Email**  
- Automatic removal of associated grades when deleting a student  

### 📘 Subjects Management
- Add, edit, and delete subjects  
- Simple table layout showing **Subject Code** and **Subject Name**  
- Automatically cleans up related grade entries upon deletion  

### 🧮 Grades Management
- Assign or update grades per student and subject  
- Automatic **GPA calculation** based on entered marks  
- Input validation (ensures valid marks between 0–100)  

### 📊 Analytics
- Integrated with **Matplotlib** to visualize average marks per subject  
- Dynamically updates based on recorded grade data  
- Displays bar chart with customizable color scheme  

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend UI** | Tkinter (ttk themed widgets) |
| **Backend Logic** | Python dictionaries and defaultdicts |
| **Charts / Analytics** | Matplotlib |
| **Theme** | Neutral gray background with blue accent tones |

---

## 🚀 How to Run

1. **Clone or download** this repository  
   ```bash
   git clone https://github.com/your-username/gradebook-management-system.git
   cd gradebook-management-system
   
2. **Install dependencies**
   ```bash
    pip install matplotlib

4. **Run the application**
   ```bash
   python gradebook_app.py


