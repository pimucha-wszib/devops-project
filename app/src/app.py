from flask import Flask, jsonify, request
from flask_migrate import Migrate
from src.db import db
from src.models import User, Task
import os

def create_app(test_config=None):
    app = Flask(__name__)
    migrate = Migrate()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/users")
    def get_users():
        users = db.session.execute(db.select(User)).scalars().all()
        return jsonify([{"id": u.id, "name": u.name} for u in users])

    @app.route("/add_user/<name>", methods=["POST"])
    def add_user(name):
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "name": user.name})

    @app.route("/users/<int:user_id>/tasks")
    def get_user_tasks(user_id):
        user = db.get_or_404(User, user_id, description="User not found")
        tasks = [{"id": t.id, "title": t.title} for t in user.tasks]
        return jsonify(tasks)

    @app.route("/add_task/<int:user_id>", methods=['POST'])
    def add_task(user_id):
        user = db.get_or_404(User, user_id, description="User not found")
        task_title = request.get_json().get("title")
        if not task_title:
            return jsonify({"error": "Task title is required"}), 400
        task = Task(title=task_title, user_id=user.id)
        db.session.add(task)
        db.session.commit()
        return jsonify({"id": task.id, "title": task.title})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
