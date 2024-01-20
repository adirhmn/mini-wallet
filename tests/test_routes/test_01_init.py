import json

def test_initialized_successfully(client):
    data = {"customer_xid":"e337aef0-b0aa-444b-8559-489603215b57"}
    response = client.post("/api/v1/init",data=json.dumps(data))

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["data"]["token"] != None

def test_failed_missing_required_field(client):
    data = {"customer":"e337aef0-b0aa-444b-8559-489603215b57"}
    response = client.post("/api/v1/init",data=json.dumps(data))
    print(response.text)

    assert response.status_code == 400
    assert response.json()["status"] == "fail"
    assert response.json()["data"]["error"]["customer_xid"] == ["Missing data for required field."]
