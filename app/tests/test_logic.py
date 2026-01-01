from src.models import User, Task
from src.db import db

def test_user_creation_logic(app):

    with app.app_context():
        user = User(name="Test User")
        db.session.add(user)
        db.session.commit()
        
        task = Task(title="Task 1", user_id=user.id)
        db.session.add(task)
        db.session.commit()

        queried_user = User.query.filter_by(name="Test User").first()
        assert queried_user is not None
        assert len(queried_user.tasks) == 1
        assert queried_user.tasks[0].title == "Task 1"
