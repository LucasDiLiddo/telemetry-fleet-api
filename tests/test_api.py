def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_register_and_login_flow(client):
    # 1. Registro
    user_payload = {
        "email": "testdriver@example.com",
        "full_name": "Test Driver",
        "role": "operator",
        "is_active": True,
        "password": "securepassword123"
    }
    res_reg = client.post("/api/v1/auth/register", json=user_payload)
    assert res_reg.status_code == 201
    assert res_reg.json()["email"] == user_payload["email"]
    assert "password" not in res_reg.json()

    # 2. Login
    login_data = {
        "username": user_payload["email"],
        "password": user_payload["password"]
    }
    res_login = client.post("/api/v1/auth/login", data=login_data)
    assert res_login.status_code == 200
    token = res_login.json().get("access_token")
    assert token is not None

    # 3. Endpoint protegido /me
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/v1/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["email"] == user_payload["email"]


def test_vehicle_and_telemetry_flow(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Crear vehículo
    vehicle_payload = {
        "vin": "1HGCR2F83HA999999",
        "plate_number": "AG999ZZ",
        "brand": "Ford",
        "model_name": "Ranger",
        "status": "active"
    }
    res_veh = client.post("/api/v1/vehicles/", json=vehicle_payload, headers=headers)
    assert res_veh.status_code == 201
    vehicle_id = res_veh.json()["id"]

    # 2. Ingestar telemetría
    telemetry_1 = {
        "vehicle_id": vehicle_id,
        "speed": 60.0,
        "fuel_level": 80.0,
        "engine_temp": 85.0,
        "latitude": -31.42,
        "longitude": -64.18
    }
    telemetry_2 = {
        "vehicle_id": vehicle_id,
        "speed": 100.0,
        "fuel_level": 75.0,
        "engine_temp": 90.0,
        "latitude": -31.43,
        "longitude": -64.19
    }
    res_t1 = client.post("/api/v1/telemetry/", json=telemetry_1, headers=headers)
    res_t2 = client.post("/api/v1/telemetry/", json=telemetry_2, headers=headers)
    assert res_t1.status_code == 201
    assert res_t2.status_code == 201

    # 3. Obtener métricas agregadas
    res_stats = client.get(f"/api/v1/telemetry/{vehicle_id}/stats", headers=headers)
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["total_records"] == 2
    assert stats["avg_speed"] == 80.0
    assert stats["max_speed"] == 100.0
    assert stats["current_fuel"] == 75.0