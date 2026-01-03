import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import User, Task


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/app_db")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/seed_output")

# Create engine and session with no flask context
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create tables if they don't exist
User.metadata.create_all(engine)
Task.metadata.create_all(engine)

names = ["Alicja", "Bogdan", "Cecylia", "Damian", "Edyta", "Filip", "Grażyna", "Hubert"]

# Find which names already exist in the database
existing = {u.name for u in session.query(User).filter(User.name.in_(names)).all()}
to_create = [n for n in names if n not in existing]

if not to_create:
    print("No new users to create. Seed skipped.")
    with open(f"{OUTPUT_DIR}/seed.log", "a") as f:
        f.write("---------------------------------\n")
        f.write(f"No new users were created at {datetime.now()}.\n")
        f.write("---------------------------------\n")
    session.close()
    exit(0)

print(f"Creating {len(to_create)} new users: {to_create}")

new_users = [User(name=n) for n in to_create]
session.add_all(new_users)
session.commit()

created = session.query(User).filter(User.name.in_(to_create)).all()

for u in created:
    session.add(Task(title=f"Task 1 for {u.name}", user_id=u.id))
    session.add(Task(title=f"Task 2 for {u.name}", user_id=u.id))
session.commit()

with open(f"{OUTPUT_DIR}/seed.log", "a") as f:
    f.write("---------------------------------\n")
    f.write(f"Database updated at {datetime.now()} with {len(created)} new users\n")
    f.write(f"More details added in file data.json\n")
    f.write("---------------------------------\n")

with open(f"{OUTPUT_DIR}/data.json", "w") as f:
    json.dump([{
                "id": u.id,
                "name": u.name,
                "tasks": [t.title for t in u.tasks]}
            for u in session.query(User).filter(User.name.in_(to_create)).all()],
        f,
        indent=2
    )

session.close()
print("Seed completed successfully.")
