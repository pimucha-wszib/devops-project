import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import User, Task


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/seed_output")

# Create engine and session with no flask context
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create tables if they don't exist
User.metadata.create_all(engine)
Task.metadata.create_all(engine)

# Check if any user data exists
if session.query(User).count() > 0:
    print("Seed skipped: data already exists in the database.")
    with open(f"{OUTPUT_DIR}/seed.log", "a") as f:
        f.write("---------------------------------\n")
        f.write(f"No actions were processed at {datetime.now()}. Database already populated.\n")
        f.write("---------------------------------\n")
    session.close()
    exit(0)

print("No data found, proceeding with seeding...")

names = ["Alicja", "Bogdan", "Cecylia", "Damian", "Edyta", "Filip", "Grażyna", "Hubert"]
users = [User(name=n) for n in names]
session.add_all(users)
session.commit()


for u in users:
    session.add(Task(title=f"Task 1 for {u.name}", user_id=u.id))
    session.add(Task(title=f"Task 2 for {u.name}", user_id=u.id))
session.commit()


with open(f"{OUTPUT_DIR}/seed.log", "a") as f:
    f.write("---------------------------------\n")
    f.write(f"Database populated at {datetime.now()} with {len(users)} new users\n")
    f.write(f"More details added in file data.json\n")
    f.write("---------------------------------\n")

with open(f"{OUTPUT_DIR}/data.json", "w") as f:
    json.dump([{
                "id": u.id,
                "name": u.name,
                "tasks": [t.title for t in u.tasks]}
            for u in session.query(User).all()],
        f,
        indent=2
    )

session.close()
print("Seed completed successfully.")
