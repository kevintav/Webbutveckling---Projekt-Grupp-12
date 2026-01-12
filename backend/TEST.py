import asyncio
from backend.services.salary_service import fetch_salary_distribution

async def main():
    result = await fetch_salary_distribution("1540")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
