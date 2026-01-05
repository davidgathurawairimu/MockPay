import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime, timedelta

class Employee:
    department_rules = {
        "IT": {"base_rate": 800, "bonus": 0.10, "shifts": {1: "9 AM - 5 PM"}},
        "HR": {"base_rate": 600, "bonus": 0.05, "shifts": {1: "8 AM - 4 PM"}},
        "Finance": {"base_rate": 700, "bonus": 0.08, "shifts": {1: "8 AM - 4 PM", 2: "4 PM - 12 AM"}},
        "Operations": {"base_rate": 500, "bonus": 0.12, "shifts": {1: "6 AM - 2 PM", 2: "2 PM - 10 PM"}},
        "Sales": {"base_rate": 550, "bonus": 0.15, "shifts": {1: "10 AM - 6 PM"}},
        "Customer Service": {"base_rate": 450, "bonus": 0.05, "shifts": {1: "8 AM - 4 PM", 2: "4 PM - 12 AM", 3: "12 AM - 8 AM"}}
    }

    job_titles = ["Software Engineer", "HR Specialist", "Financial Analyst", 
                  "Operations Manager", "Sales Executive", "Customer Support Rep"]

    locations = ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru", "Thika"]
    genders = ["Male", "Female", "Non-binary"]
    statuses = ["Full-time", "Part-time"]

    def __init__(self, emp_id, name, department, shift=None):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        rules = Employee.department_rules.get(department, {"base_rate": 400, "bonus": 0, "shifts": {1: "8 AM - 4 PM"}})
        self.hourly_rate = rules["base_rate"]
        self.shift = shift if shift else random.choice(list(rules["shifts"].keys()))
        self.shift_time = rules["shifts"][self.shift]
        self.hours_worked = random.randint(120, 180)
        self.bonus_rate = rules["bonus"]

        # New fields
        self.job_title = random.choice(Employee.job_titles)
        self.hire_date = datetime.now() - timedelta(days=random.randint(30, 3650))  # up to 10 years ago
        self.status = random.choice(Employee.statuses)
        self.age = random.randint(22, 60)
        self.gender = random.choice(Employee.genders)
        self.location = random.choice(Employee.locations)

    def calculate_pay(self):
        base_pay = self.hourly_rate * self.hours_worked
        bonus = base_pay * self.bonus_rate
        return base_pay + bonus

    def to_dict(self):
        return {
            "ID": f"{self.emp_id:03d}",
            "Name": self.name,
            "Department": self.department,
            "Job Title": self.job_title,
            "Hire Date": self.hire_date.strftime("%Y-%m-%d"),
            "Status": self.status,
            "Age": self.age,
            "Gender": self.gender,
            "Location": self.location,
            "Shift": self.shift_time,
            "Hours Worked": self.hours_worked,
            "Hourly Rate": self.hourly_rate,
            "Monthly Pay": round(self.calculate_pay(), 2)
        }

def generate_random_name():
    first_names = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","William","Elizabeth","David","Susan"]
    last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

class PayrollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll Simulation")
        self.root.geometry("1200x750")

        # Expandable layout
        self.root.rowconfigure(2, weight=1)
        for col in range(4):
            self.root.columnconfigure(col, weight=1)

        # Input field
        tk.Label(root, text="Number of Employees:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.num_entry = tk.Entry(root)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        tk.Button(root, text="Generate", command=self.start_generation).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="Export CSV", command=self.export_csv).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=1, column=0, columnspan=4, pady=10)

        # Table with scrollbar
        frame = tk.Frame(root)
        frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(frame, columns=("ID","Name","Department","Job Title","Hire Date","Status","Age","Gender","Location","Shift","Hours Worked","Hourly Rate","Monthly Pay"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # State
        self.employees = []
        self.total_to_generate = 0
        self.current_index = 0

    def start_generation(self):
        try:
            self.total_to_generate = int(self.num_entry.get())
            self.employees = []
            self.current_index = 0
            # clear table
            for row in self.tree.get_children():
                self.tree.delete(row)
            # reset progress bar
            self.progress["value"] = 0
            self.progress["maximum"] = self.total_to_generate
            # start progressive generation
            self.generate_next_employee()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def generate_next_employee(self):
        if self.current_index < self.total_to_generate:
            emp = Employee(self.current_index+1, generate_random_name(), random.choice(list(Employee.department_rules.keys())))
            self.employees.append(emp)
            data = emp.to_dict()
            self.tree.insert("", "end", values=tuple(data.values()))
            self.current_index += 1
            # update progress bar
            self.progress["value"] = self.current_index
            # schedule next employee after 150ms
            self.root.after(150, self.generate_next_employee)

    def export_csv(self):
        if not self.employees:
            messagebox.showwarning("Warning", "No employees to export")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(self.employees[0].to_dict().keys()))
                writer.writeheader()
                for emp in self.employees:
                    writer.writerow(emp.to_dict())
            messagebox.showinfo("Success", f"Data exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollApp(root)
    root.mainloop()
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime, timedelta

class Employee:
    department_rules = {
        "IT": {"base_rate": 800, "bonus": 0.10, "shifts": {1: "9 AM - 5 PM"}},
        "HR": {"base_rate": 600, "bonus": 0.05, "shifts": {1: "8 AM - 4 PM"}},
        "Finance": {"base_rate": 700, "bonus": 0.08, "shifts": {1: "8 AM - 4 PM", 2: "4 PM - 12 AM"}},
        "Operations": {"base_rate": 500, "bonus": 0.12, "shifts": {1: "6 AM - 2 PM", 2: "2 PM - 10 PM"}},
        "Sales": {"base_rate": 550, "bonus": 0.15, "shifts": {1: "10 AM - 6 PM"}},
        "Customer Service": {"base_rate": 450, "bonus": 0.05, "shifts": {1: "8 AM - 4 PM", 2: "4 PM - 12 AM", 3: "12 AM - 8 AM"}}
    }

    job_titles = ["Software Engineer", "HR Specialist", "Financial Analyst", 
                  "Operations Manager", "Sales Executive", "Customer Support Rep"]

    locations = ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru", "Thika"]
    genders = ["Male", "Female", "Non-binary"]
    statuses = ["Full-time", "Part-time"]

    def __init__(self, emp_id, name, department, shift=None):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        rules = Employee.department_rules.get(department, {"base_rate": 400, "bonus": 0, "shifts": {1: "8 AM - 4 PM"}})
        self.hourly_rate = rules["base_rate"]
        self.shift = shift if shift else random.choice(list(rules["shifts"].keys()))
        self.shift_time = rules["shifts"][self.shift]
        self.hours_worked = random.randint(120, 180)
        self.bonus_rate = rules["bonus"]

        # New fields
        self.job_title = random.choice(Employee.job_titles)
        self.hire_date = datetime.now() - timedelta(days=random.randint(30, 3650))  # up to 10 years ago
        self.status = random.choice(Employee.statuses)
        self.age = random.randint(22, 60)
        self.gender = random.choice(Employee.genders)
        self.location = random.choice(Employee.locations)

    def calculate_pay(self):
        base_pay = self.hourly_rate * self.hours_worked
        bonus = base_pay * self.bonus_rate
        return base_pay + bonus

    def to_dict(self):
        return {
            "ID": f"{self.emp_id:03d}",
            "Name": self.name,
            "Department": self.department,
            "Job Title": self.job_title,
            "Hire Date": self.hire_date.strftime("%Y-%m-%d"),
            "Status": self.status,
            "Age": self.age,
            "Gender": self.gender,
            "Location": self.location,
            "Shift": self.shift_time,
            "Hours Worked": self.hours_worked,
            "Hourly Rate": self.hourly_rate,
            "Monthly Pay": round(self.calculate_pay(), 2)
        }

def generate_random_name():
    first_names = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","William","Elizabeth","David","Susan"]
    last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

class PayrollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll Simulation")
        self.root.geometry("1200x900")

        # Expandable layout
        self.root.rowconfigure(4, weight=1)
        for col in range(4):
            self.root.columnconfigure(col, weight=1)

        # Input field
        tk.Label(root, text="Number of Employees:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.num_entry = tk.Entry(root)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        tk.Button(root, text="Generate", command=self.start_generation).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="Export CSV", command=self.export_csv).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=1, column=0, columnspan=4, pady=10)

        # Table with scrollbar
        frame = tk.Frame(root)
        frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(frame, columns=("ID","Name","Department","Job Title","Hire Date","Status","Age","Gender","Location","Shift","Hours Worked","Hourly Rate","Monthly Pay"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # ✅ Summary panel
        summary_frame = tk.LabelFrame(root, text="Payroll Summary", padx=10, pady=10)
        summary_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

        self.total_payroll_label = tk.Label(summary_frame, text="Total Payroll: Kshs 0.00")
        self.total_payroll_label.grid(row=0, column=0, sticky="w")

        self.avg_payroll_label = tk.Label(summary_frame, text="Average Pay per Department: -")
        self.avg_payroll_label.grid(row=0, column=1, sticky="w")

        self.highest_label = tk.Label(summary_frame, text="Highest Earner: -")
        self.highest_label.grid(row=1, column=0, sticky="w")

        self.lowest_label = tk.Label(summary_frame, text="Lowest Earner: -")
        self.lowest_label.grid(row=1, column=1, sticky="w")

        # ✅ Filter panel
        filter_frame = tk.LabelFrame(root, text="Filters", padx=10, pady=10)
        filter_frame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

        tk.Label(filter_frame, text="Department:").grid(row=0, column=0, padx=5, pady=5)
        self.dept_choice = ttk.Combobox(filter_frame, values=["All"] + list(Employee.department_rules.keys()))
        self.dept_choice.current(0)
        self.dept_choice.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Status:").grid(row=0, column=2, padx=5, pady=5)
        self.status_choice = ttk.Combobox(filter_frame, values=["All"] + Employee.statuses)
        self.status_choice.current(0)
        self.status_choice.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter).grid(row=0, column=4, padx=5, pady=5)

        # State
        self.employees = []
        self.total_to_generate = 0
        self.current_index = 0

    def start_generation(self):
        try:
            self.total_to_generate = int(self.num_entry.get())
            self.employees = []
            self.current_index = 0
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.progress["value"] = 0
            self.progress["maximum"] = self.total_to_generate
            self.generate_next_employee()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def generate_next_employee(self):
        if self.current_index < self.total_to_generate:
            emp = Employee(self.current_index+1, generate_random_name(), random.choice(list(Employee.department_rules.keys())))
            self.employees.append(emp)
            data = emp.to_dict()
            self.tree.insert("", "end", values=tuple(data.values()))
            self.current
