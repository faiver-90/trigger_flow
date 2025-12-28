def test_validation_exception(sync_client):
    response = sync_client.get("/validation-error")  # не передаём limit -> 422
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 422
    assert data["message"] == "Validation failed"
    assert "errors" in data


def test_http_exception_handler(sync_client):
    response = sync_client.get("/http-error")
    assert response.status_code == 403
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 403
    assert data["message"] == "Forbidden action"


def test_generic_exception_handler(sync_client):
    response = sync_client.get("/unexpected-error")
    assert response.status_code == 500
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 500
    assert "Internal server error" in data["message"]
