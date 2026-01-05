# MockPay
A Tkinter-based payroll simulator that generates mock employee data with demographics, job details, progressive loading, filters, and summary panels. Designed for HR training, it helps staff practice payroll analysis, exporting subsets, and visualizing workforce insights safely with synthetic data.

✨ Features
Mock Employee Data Generation

Random names, departments, job titles, hire dates, statuses (Full-time/Part-time).

Demographic diversity: age, gender, location.

Shift assignments and hours worked.

Progressive Loading

Employees appear one by one with a progress bar showing generation status.

Interactive Table

Scrollable Tkinter Treeview with employee details.

Columns include ID, Name, Department, Job Title, Hire Date, Status, Age, Gender, Location, Shift, Hours Worked, Hourly Rate, Monthly Pay.

Filters

Filter employees by Department or Status using dropdowns.

Apply filters to view subsets directly in the table.

Summary Panels

Total Payroll across all employees.

Average Pay per Department.

Highest Earner with name, department, and pay.

Lowest Earner with name, department, and pay.

Export Options

Export all employees or filtered subsets to CSV.

Safe synthetic data for training and testing.

📑 Data Dictionary – Payroll Simulator Dataset
Column Name	Description
ID	Unique employee identifier (e.g., 001, 002).
Name	Randomly generated employee full name.
Department	Assigned department (IT, HR, Finance, Operations, Sales, Customer Service).
Job Title	Randomly assigned role within the department (e.g., Software Engineer).
Hire Date	Synthetic hire date within the last 10 years.
Status	Employment type: Full-time or Part-time.
Age	Randomly generated age (22–60).
Gender	Randomly assigned gender (Male, Female, Non-binary).
Location	Randomly assigned city (Nairobi, Mombasa, Kisumu, Eldoret, Nakuru, Thika).
Shift	Assigned work shift (e.g., 9 AM – 5 PM).
Hours Worked	Monthly hours worked (random between 120–180).
Hourly Rate	Base hourly rate determined by department rules.
Monthly Pay	Calculated pay = (Hourly Rate × Hours Worked) + Department Bonus.
