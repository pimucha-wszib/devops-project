
def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_add_user_endpoint(client):
    response = client.post('/add_user/Marek')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["name"] == "Marek"
    assert "id" in data

def test_add_task_validation(client):
    client.post('/add_user/Ania')

    response = client.post('/add_task/1', json={})
    
    assert response.status_code == 400
    assert response.get_json()["error"] == "Task title is required"

def test_get_user_tasks_not_found(client):
    response = client.get('/users/999/tasks')
    assert response.status_code == 404

def test_add_task_success(client):
    client.post('/add_user/Janek')

    response = client.post('/add_task/1', json={"title": "New Task"})
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["title"] == "New Task"
    assert "id" in data

    response = client.get('/users/1/tasks')
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "New Task"
