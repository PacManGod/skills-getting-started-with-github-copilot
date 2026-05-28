from urllib.parse import quote

from src.app import activities


def test_get_activities_structure(client):
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert expected_keys.issubset(data["Chess Club"].keys())
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_delete_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name)}/participants"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_signup_invalid_activity_returns_404(client):
    # Arrange
    activity_name = "No Such Club"
    email = "teststudent@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"