from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_task_crud_and_bot_flow():
    create = client.post(
        "/tasks",
        json={
            "title": "Investigate queue drift",
            "description": "Mismatch between producer and consumer throughput",
            "owner": "ops",
            "priority": "medium",
        },
    )
    assert create.status_code == 201
    task_id = create.json()["id"]

    patch = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert patch.status_code == 200
    assert patch.json()["status"] == "in_progress"

    bot = client.post("/bot/command", json={"command": f"complete {task_id}"})
    assert bot.status_code == 200
    assert bot.json()["ok"] is True

    get_task = client.get(f"/tasks/{task_id}")
    assert get_task.status_code == 200
    assert get_task.json()["status"] == "completed"
