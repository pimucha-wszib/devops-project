from src.app import create_app
from src.db import db
from flask_migrate import upgrade, Migrate

app = create_app()
migrate = Migrate()

with app.app_context():

    migrate.init_app(app, db)
    print("Performing migrations...")

    try:
        upgrade()
        print("Migrations complete.")
    except Exception as e:
        print(f"Migration failed: {e}")
        exit(1)