import csv 
import os 
from datetime import datetime


file = "/app/data/app_status.csv"

headers = [
    "Date Submitted",
    "Company Name",
    "Job Title",
    "Salary",
    "Response"
]

if not os.path.exists(file):
    with open(file, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
else:
    print(f"File {file} already exists")

def add_application():
    date_submitted = datetime.today().strftime("%Y-%m-%d")
    company_name = input("Company Name?: ")
    job_title = input("Job Title?: ")
    salary = input("Salary?: ")
    app_response = input("Applied, Interviewing, Rejected?: ")
        
    with open(file, "a", newline = "", encoding = "utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([date_submitted, company_name, job_title, salary, app_response])

def update_status():
    company_name = input("Company Name?: ")
    job_title = input("Job Title?: ")
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for row in rows:
        if row["Company Name"] == company_name and row["Job Title"] == job_title:
            row["Response"] = input("What is the current status?: ")
    with open(file, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames = headers)
        writer.writeheader()
        writer.writerows(rows)

def search():
    company_name = input("Company Name?: ")
    job_title = input("Job Title?: ")
    found = False
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for row in rows:
        if row["Company Name"] == company_name and row["Job Title"] == job_title:
            found = True
            print(f"\n Here is the job you are looking for:\n\n Date Submitted: {row["Date Submitted"]}\n Company Name: {row["Company Name"]}\n Job Title: {row["Job Title"]}\n Salary: {row["Salary"]}\n Response: {row["Response"]}")
    if not found:
            print("No Results Found.")
                
def view_all():
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for row in rows:
        print(f"Company Name: {row["Company Name"]}\n Job Title: {row["Job Title"]}\n Response: {row["Response"]}")
        print("-" * 30)

            


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

