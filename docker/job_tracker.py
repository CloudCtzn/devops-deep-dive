import os
import psycopg2  
from datetime import datetime


def get_connection():
    return psycopg2.connect(
        host = os.environ.get("DB_HOST", "localhost"),
        dbname = os.environ.get("DB_NAME", "jobtracker"),
        user = os.environ.get("DB_USER", "postgres"),
        password = os.environ.get("DB_PASSWORD", "postgres")
        )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS applications(
                id SERIAL PRIMARY KEY,
                date_submitted DATE,
                company_name VARCHAR(100),
                job_title VARCHAR(100),
                salary VARCHAR(50),
                response VARCHAR(50)
                )
            """)
    conn.commit()
    cur.close()
    conn.close()

def add_application():
    date_submitted = datetime.today().strftime("%Y-%m-%d")
    company_name = input("Company Name?: ")
    job_title = input("Job Title?: ")
    salary = input("Salary?: ")
    app_response = input("Applied, Interviewing, Rejected?: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO applications (date_submitted, company_name, job_title, salary, response)
        VALUES (%s, %s, %s, %s, %s)
        """, (date_submitted, company_name, job_title, salary, app_response))
    conn.commit()
    cur.close()
    conn.close()
    print("Application added.")

def update_status():
    company_name = input("Company Name?: ")
    job_title = input("Job Title?: ")
    new_status = input("What is the current status?: ")
    

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE applications
        SET response = %s
        WHERE  company_name = %s AND job_title = %s
        """, (new_status, company_name, job_title))
    conn.commit()
    cur.close()
    conn.close()
    print("Status Updated.")

def search():
    company_name = input("Company Name?: ")
    job_title = input("Job Title?: ")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT date_submitted, company_name, job_title, salary, response
        FROM applications
        WHERE company_name = %s AND job_title = %s
        """, (company_name, job_title))
    row = cur.fetchone()
    if row:
        print(f"\nDate Submitted: {row[0]}\nCompany Name: {row[1]}\nJob Title: {row[2]}\nSalary: {row[3]}\nResponse: {row[4]}")
    else:
        print("No Results Found.")
    cur.close()
    conn.close()
                
def view_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT date_submitted, company_name, job_title, salary, response FROM applications")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for row in rows:
        print(f"\nDate Submitted: {row[0]}\nCompany Name: {row[1]}\nJob Title: {row[2]}\nSalary: {row[3]}\nResponse: {row[4]}")
        print("-" * 30)

init_db()

while True:
    print("\n1. Add Application\n2. Update Status\n3. Search\n4. View All\n5. Quit")
    response = int(input())
    if response == 1:
        add_application()
    elif response ==2:
        update_status()
    elif response == 3:
        search()
    elif response == 4:
        view_all()
    elif response == 5:
        break
    else:
        print("Please choose a menu option.")

