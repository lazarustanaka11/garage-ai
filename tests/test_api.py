from fastapi.testclient import TestClient


def register_and_login(client: TestClient) -> dict[str, str]:
    registration = client.post(
        "/api/auth/register",
        json={
            "email": "owner@example.com",
            "password": "secure-password",
            "full_name": "Garage Owner",
        },
    )
    assert registration.status_code == 201

    login = client.post(
        "/api/auth/login",
        data={
            "username": "owner@example.com",
            "password": "secure-password",
        },
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def create_customer(client: TestClient, headers: dict[str, str]) -> dict:
    response = client.post(
        "/api/customers",
        headers=headers,
        json={
            "name": "Jamie Customer",
            "email": "jamie@example.com",
            "phone": "555-0100",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/api")

    assert response.status_code == 200
    assert response.json() == {
        "application": "Garage AI",
        "version": "1.0.0",
        "status": "running",
    }


def test_auth_register_login_and_current_user(client: TestClient) -> None:
    headers = register_and_login(client)

    response = client.get("/api/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == "owner@example.com"
    assert response.json()["full_name"] == "Garage Owner"
    assert "hashed_password" not in response.json()


def test_auth_rejects_duplicate_registration_and_bad_password(
    client: TestClient,
) -> None:
    register_and_login(client)

    duplicate = client.post(
        "/api/auth/register",
        json={
            "email": "owner@example.com",
            "password": "another-password",
            "full_name": "Duplicate Owner",
        },
    )
    invalid_login = client.post(
        "/api/auth/login",
        data={
            "username": "owner@example.com",
            "password": "wrong-password",
        },
    )

    assert duplicate.status_code == 400
    assert duplicate.json()["detail"] == "A user with this email already exists."
    assert invalid_login.status_code == 401


def test_protected_endpoint_requires_authentication(
    client: TestClient,
) -> None:
    response = client.get("/api/customers")

    assert response.status_code == 401


def test_customer_crud_and_duplicate_email(
    client: TestClient,
) -> None:
    headers = register_and_login(client)
    customer = create_customer(client, headers)
    customer_id = customer["id"]

    listing = client.get("/api/customers", headers=headers)
    fetched = client.get(f"/api/customers/{customer_id}", headers=headers)
    updated = client.put(
        f"/api/customers/{customer_id}",
        headers=headers,
        json={
            "name": "Jamie Updated",
            "email": "jamie.updated@example.com",
            "phone": "555-0199",
        },
    )
    duplicate = client.post(
        "/api/customers",
        headers=headers,
        json={
            "name": "Another Customer",
            "email": "jamie.updated@example.com",
            "phone": "555-0101",
        },
    )

    assert listing.status_code == 200
    assert len(listing.json()) == 1
    assert fetched.status_code == 200
    assert updated.status_code == 200
    assert updated.json()["name"] == "Jamie Updated"
    assert duplicate.status_code == 400
    assert duplicate.json()["detail"] == "A customer with this email already exists."

    deleted = client.delete(f"/api/customers/{customer_id}", headers=headers)
    missing = client.get(f"/api/customers/{customer_id}", headers=headers)

    assert deleted.status_code == 204
    assert missing.status_code == 404


def test_vehicle_creation_validates_customer_and_unique_identifiers(
    client: TestClient,
) -> None:
    headers = register_and_login(client)
    customer = create_customer(client, headers)
    vehicle_payload = {
        "customer_id": customer["id"],
        "make": "Honda",
        "model": "Accord",
        "year": 2020,
        "vin": "1HGCM82633A004352",
        "license_plate": "GARAGE-1",
        "mileage": 42000,
        "color": "Blue",
        "last_service_date": None,
    }
    created = client.post(
        "/api/vehicles",
        headers=headers,
        json=vehicle_payload,
    )
    duplicate_vin = client.post(
        "/api/vehicles",
        headers=headers,
        json={**vehicle_payload, "license_plate": "GARAGE-2"},
    )
    missing_customer = client.post(
        "/api/vehicles",
        headers=headers,
        json={**vehicle_payload, "customer_id": "00000000-0000-0000-0000-000000000001"},
    )

    assert created.status_code == 201
    assert created.json()["vin"] == vehicle_payload["vin"]
    assert duplicate_vin.status_code == 400
    assert duplicate_vin.json()["detail"] == "VIN already exists."
    assert missing_customer.status_code == 400
    assert missing_customer.json()["detail"] == "Customer not found."


def test_repair_job_creation_and_completion_workflow(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    customer = create_customer(client, auth_headers)
    vehicle_response = client.post(
        "/api/vehicles",
        headers=auth_headers,
        json={
            "customer_id": customer["id"],
            "make": "Toyota",
            "model": "Corolla",
            "year": 2021,
            "vin": "2T1BURHE0JC123456",
            "license_plate": "GARAGE-3",
            "mileage": 25000,
            "color": "White",
            "last_service_date": None,
        },
    )
    assert vehicle_response.status_code == 201
    vehicle_id = vehicle_response.json()["id"]

    missing_vehicle = client.post(
        "/api/repair-jobs",
        headers=auth_headers,
        json={
            "vehicle_id": "00000000-0000-0000-0000-000000000001",
            "title": "Brake inspection",
            "description": "Customer hears a squeal while braking.",
            "mileage": 25000,
        },
    )
    created = client.post(
        "/api/repair-jobs",
        headers=auth_headers,
        json={
            "vehicle_id": vehicle_id,
            "title": "Brake inspection",
            "description": "Customer hears a squeal while braking.",
            "mileage": 25000,
        },
    )

    assert missing_vehicle.status_code == 400
    assert created.status_code == 201
    assert created.json()["status"] == "OPEN"
    repair_job_id = created.json()["id"]
    completed_payload = {
        "title": "Brake inspection",
        "description": "Customer hears a squeal while braking.",
        "mileage": 25000,
        "technician_notes": "Front brake pads replaced.",
        "ai_diagnosis": None,
        "status": "COMPLETED",
    }

    completed = client.put(
        f"/api/repair-jobs/{repair_job_id}",
        headers=auth_headers,
        json=completed_payload,
    )
    repeated_completion = client.put(
        f"/api/repair-jobs/{repair_job_id}",
        headers=auth_headers,
        json=completed_payload,
    )
    missing_job = client.get(
        "/api/repair-jobs/00000000-0000-0000-0000-000000000001",
        headers=auth_headers,
    )

    assert completed.status_code == 200
    assert completed.json()["status"] == "COMPLETED"
    assert completed.json()["completed_at"] is not None
    assert completed.json()["technician_notes"] == "Front brake pads replaced."
    assert repeated_completion.status_code == 400
    assert repeated_completion.json()["detail"] == "Repair job is already completed."
    assert missing_job.status_code == 404
