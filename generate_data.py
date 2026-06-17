from faker import Faker
import pandas as pd
import random

fake = Faker()

degrees = [
    "Computer Science", "Information Systems", "Data Science",
    "B Com Accounting", "Education", "Civil Engineering", "Law", "Marketing"
    ]

companies = [
    "Standard Bank", "Capitec", "Discovery", "Deloitte",
    "Amazon", "Accenture", "Vodacom", "Shoprite", "Takealot"
]

skills = [
    "Python", "SQL", "PowerBI", "Excel", "Java", "Cloud Computing",
    "Machine Learning", "Communication"
]

graduates = []

for i in range(1000):
    employed = random.choice([True, False])

    graduate = {
        "graduate_id": i + 1,
        "name": fake.name(),
        "age": random.randint(21, 35),
        "gender": random.choice(["Male", "Female"]),
        "degree": random.choice(degrees),
        "graduation_year": random.choice([2023, 2024, 2025]),
        "employed": employed,
        "company": random.choice(companies) if employed else None,
        "salary": random.randint(15000, 60000) if employed else None,
        "months_to_employment":
            random.randint(1, 12) if employed else None,
        "skill": random.choice(skills)
    }

    graduates.append(graduate)

df = pd.DataFrame(graduates)

df.to_csv("data/graduate_survey.csv", index=False)

print("Dataset created successfully!")
print(df.head())
