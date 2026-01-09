from backend.services.jobs_service import fetch_jobs
from backend.services.salary_service import fetch_salary

print("Salary:", fetch_salary("2511").get("average_salary"))
print("Contacts:", fetch_jobs("Frontend", "Stockholm")[0].get("contacts"))
