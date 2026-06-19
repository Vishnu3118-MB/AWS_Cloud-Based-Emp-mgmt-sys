from flask import Flask, render_template, request, redirect, send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import pandas as pd
import pymysql

app = Flask(__name__)

# Database Connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Root@123",
    database="employee_db"
)


# Login Page
@app.route('/')
def login():
    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():

    cursor = db.cursor()

    # Total Employees
    cursor.execute("SELECT COUNT(*) FROM employee")
    total_emp = cursor.fetchone()[0]

    # Total Departments
    cursor.execute("SELECT COUNT(*) FROM department")
    total_dept = cursor.fetchone()[0]

    # Total Payroll
    cursor.execute("SELECT IFNULL(SUM(salary),0) FROM employee")
    total_payroll = cursor.fetchone()[0]

    # Average Salary
    cursor.execute("SELECT ROUND(AVG(salary),2) FROM employee")
    avg_salary = cursor.fetchone()[0]

    # Recent Employees
    cursor.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            e.email,
            d.dept_name,
            e.designation,
            e.salary
        FROM employee e
        JOIN department d
        ON e.dept_id = d.dept_id
        ORDER BY e.emp_id DESC
        LIMIT 5
    """)

    employees = cursor.fetchall()

    # Department Wise Employee Count

    cursor.execute("""
        SELECT d.dept_name, COUNT(e.emp_id)
        FROM department d
        LEFT JOIN employee e
        ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
    """)

    dept_data = cursor.fetchall()

    dept_labels = []
    dept_counts = []

    for row in dept_data:
        dept_labels.append(row[0])
        dept_counts.append(row[1])

    # Department Wise Salary

    cursor.execute("""
        SELECT
            d.dept_name,
            IFNULL(SUM(e.salary),0)
        FROM department d
        LEFT JOIN employee e
            ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
    """)

    salary_data = cursor.fetchall()

    salary_labels = []
    salary_totals = []

    for row in salary_data:
        salary_labels.append(row[0])
        salary_totals.append(float(row[1]))

    # Highest Salary Employee
    cursor.execute("""
    SELECT emp_name, salary
    FROM employee
    ORDER BY salary DESC
    LIMIT 1
    """)
    highest_salary = cursor.fetchone()

    # Lowest Salary Employee
    cursor.execute("""
    SELECT emp_name, salary
    FROM employee
    ORDER BY salary ASC
    LIMIT 1
    """)
    lowest_salary = cursor.fetchone()

    cursor.execute("""
    SELECT
        e.emp_name,
        d.dept_name,
        e.salary
    FROM employee e
    JOIN department d
    ON e.dept_id = d.dept_id
    ORDER BY e.salary DESC
    LIMIT 5
    """)

    top_paid_employees = cursor.fetchall()

    return render_template(
        "dashboard.html",
        total_emp=total_emp,
        total_dept=total_dept,
        total_payroll=total_payroll,
        avg_salary=avg_salary,
        employees=employees,
        dept_labels=dept_labels,
        dept_counts=dept_counts,

        salary_labels=salary_labels,
        salary_totals=salary_totals,

        highest_salary=highest_salary,
        lowest_salary=lowest_salary,

        top_paid_employees=top_paid_employees
    )


# Add Employee Page
@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():

    cursor = db.cursor()

    # Load Departments
    cursor.execute("SELECT dept_id, dept_name FROM department")
    departments = cursor.fetchall()

    if request.method == 'POST':

        emp_name = request.form['emp_name']
        email = request.form['email']
        phone = request.form['phone']
        dept_id = request.form['dept_id']
        designation = request.form['designation']
        salary = request.form['salary']
        joining_date = request.form['joining_date']

        sql = """
        INSERT INTO employee
        (
            emp_name,
            email,
            phone,
            dept_id,
            designation,
            salary,
            joining_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                emp_name,
                email,
                phone,
                dept_id,
                designation,
                salary,
                joining_date
            )
        )

        db.commit()

        return redirect('/employees')

    return render_template(
        'add_employee.html',
        departments=departments
    )


# Employee List Page
@app.route('/employees')
def employees():

    search = request.args.get('search', '')

    cursor = db.cursor()

    sql = """
    SELECT
        e.emp_id,
        e.emp_name,
        e.email,
        d.dept_name,
        e.designation,
        e.salary,
        e.joining_date
    FROM employee e
    JOIN department d
        ON e.dept_id = d.dept_id
    WHERE e.emp_name LIKE %s
    ORDER BY e.emp_id
    """

    cursor.execute(
        sql,
        ('%' + search + '%',)
    )

    employee_data = cursor.fetchall()

    return render_template(
        'employee_list.html',
        employees=employee_data,
        search=search
    )

@app.route('/export-excel')
def export_excel():

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            e.email,
            d.dept_name,
            e.designation,
            e.salary,
            e.joining_date
        FROM employee e
        JOIN department d
        ON e.dept_id = d.dept_id
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            'ID',
            'Name',
            'Email',
            'Department',
            'Designation',
            'Salary',
            'Joining Date'
        ]
    )

    file_name = "employees.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )

@app.route('/export-pdf')
def export_pdf():

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            e.emp_id,
            e.emp_name,
            d.dept_name,
            e.designation,
            e.salary
        FROM employee e
        JOIN department d
        ON e.dept_id = d.dept_id
        ORDER BY e.emp_id
    """)

    employees = cursor.fetchall()

    pdfmetrics.registerFont(
        TTFont('ArialUnicode', 'arial.ttf')
    )

    pdf_file = "employee_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>EMPLOYEE MANAGEMENT SYSTEM</b>",
            styles['Title']
        )
    )

    elements.append(
        Paragraph(
            "Employee Report",
            styles['Heading2']
        )
    )

    elements.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles['Normal']
        )
    )

    elements.append(Spacer(1, 20))

    data = [
        ["ID", "Name", "Department", "Designation", "Salary"]
    ]

    for emp in employees:
        data.append([
            emp[0],
            emp[1],
            emp[2],
            emp[3],
            f"Rs. {emp[4]}"
        ])

    table = Table(
        data,
        colWidths=[40,120,90,120,80]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#6d28d9')),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,1),(-1,-1),'ArialUnicode'),
        ('FONTSIZE',(0,0),(-1,0),12),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    elements.append(table)

    elements.append(Spacer(1,20))

    cursor.execute(
        "SELECT IFNULL(SUM(salary),0) FROM employee"
    )
    total_payroll = cursor.fetchone()[0]

    cursor.execute(
        "SELECT ROUND(AVG(salary),2) FROM employee"
    )
    avg_salary = cursor.fetchone()[0]

    elements.append(
        Paragraph(
            f"<b>Total Employees:</b> {len(employees)}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Payroll:</b> Rs. {total_payroll}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Average Salary:</b> Rs. {avg_salary}",
            styles['Normal']
        )
    )

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            "Generated by Employee Management System",
            styles['Italic']
        )
    )

    doc.build(elements)

    return send_file(
        pdf_file,
        as_attachment=True
    )


# Edit Employee Page
@app.route('/edit-employee/<int:emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):

    cursor = db.cursor()

    # Load departments
    cursor.execute("SELECT dept_id, dept_name FROM department")
    departments = cursor.fetchall()

    if request.method == 'POST':

        emp_name = request.form['emp_name']
        email = request.form['email']
        phone = request.form['phone']
        dept_id = request.form['dept_id']
        designation = request.form['designation']
        salary = request.form['salary']
        joining_date = request.form['joining_date']

        update_sql = """
        UPDATE employee
        SET
            emp_name = %s,
            email = %s,
            phone = %s,
            dept_id = %s,
            designation = %s,
            salary = %s,
            joining_date = %s
        WHERE emp_id = %s
        """

        cursor.execute(
            update_sql,
            (
                emp_name,
                email,
                phone,
                dept_id,
                designation,
                salary,
                joining_date,
                emp_id
            )
        )

        db.commit()

        return redirect('/employees')

    cursor.execute(
        "SELECT * FROM employee WHERE emp_id = %s",
        (emp_id,)
    )

    employee = cursor.fetchone()

    return render_template(
        'edit_employee.html',
        employee=employee,
        departments=departments
    )

@app.route('/delete-employee/<int:emp_id>')
def delete_employee(emp_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM employee WHERE emp_id = %s",
        (emp_id,)
    )

    db.commit()

    return redirect('/employees')


if __name__ == '__main__':
    app.run(debug=True)