import json
from fastapi.testclient import TestClient

customer_xid = "e337aef0-b0aa-444b-8559-489603215b57"
reference_id_deposit = "50535246-dcb2-4929-8cc9-004ea06f5291"
reference_id_withdrawal = "50535246-dcb2-4929-8cc9-004ea06f5293"
deposit_amount = 10000
withdrawal_amount = 3000
current_balance = deposit_amount - withdrawal_amount

def get_token(client: TestClient):
    data = {"customer_xid":customer_xid}
    response = client.post("/api/v1/init",data=json.dumps(data))
    return response.json()["data"]["token"]

def test_enabled_successfully(client):
    data = {"customer_xid":customer_xid}
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.post("/api/v1/wallet", data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["data"]["wallet"]["id"] != None
    assert response.json()["data"]["wallet"]["owned_by"] == customer_xid
    assert response.json()["data"]["wallet"]["status"] == "enabled"
    assert response.json()["data"]["wallet"]["enabled_at"] != None
    assert response.json()["data"]["wallet"]["balance"] == 0

def test_failed_as_already_enabled(client):
    data = {"customer_xid":customer_xid}
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.post("/api/v1/wallet", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json()["status"] == "fail"
    assert response.json()["data"]["error"] == "Already enabled"

def test_added_money_successfully(client):
    reference_id = reference_id_deposit
    amount = deposit_amount
    data = {"amount":amount, "reference_id":reference_id}
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.post("/api/v1/wallet/deposits", data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    assert response.json()["data"]["deposit"]["id"] != None
    assert response.json()["data"]["deposit"]["deposited_by"] == customer_xid
    assert response.json()["data"]["deposit"]["status"] == "success"
    assert response.json()["data"]["deposit"]["deposited_at"] != None
    assert response.json()["data"]["deposit"]["amount"] == amount
    assert response.json()["data"]["deposit"]["reference_id"] == reference_id

def test_withdrawn_successfully(client):
    reference_id = reference_id_withdrawal
    amount = withdrawal_amount
    data = {"amount":amount, "reference_id":reference_id}
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.post("/api/v1/wallet/withdrawals", data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    assert response.json()["data"]["deposit"]["id"] != None
    assert response.json()["data"]["deposit"]["withdrawn_by_by"] == customer_xid
    assert response.json()["data"]["deposit"]["status"] == "success"
    assert response.json()["data"]["deposit"]["withdrawn_by_at"] != None
    assert response.json()["data"]["deposit"]["amount"] == amount
    assert response.json()["data"]["deposit"]["reference_id"] == reference_id

def test_view_wallet_successfully(client):
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.get("/api/v1/wallet", headers=headers)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["wallet"]["id"] != None
    assert response.json()["data"]["wallet"]["owned_by"] == customer_xid
    assert response.json()["data"]["wallet"]["status"] == "enabled"
    assert response.json()["data"]["wallet"]["enabled_at"] != None
    assert response.json()["data"]["wallet"]["balance"] == current_balance

def test_view_transactions_successfully(client):
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.get("/api/v1/wallet/transactions", headers=headers)

    assert response.status_code == 200
    assert response.json()["data"]["transactions"][0]["id"] != None
    assert response.json()["data"]["transactions"][0]["status"] == "success"
    assert response.json()["data"]["transactions"][0]["transacted_at"] != None
    assert response.json()["data"]["transactions"][0]["type"] == "withdrawal"
    assert response.json()["data"]["transactions"][0]["amount"] == withdrawal_amount
    assert response.json()["data"]["transactions"][0]["reference_id"] == reference_id_withdrawal
    assert response.json()["data"]["transactions"][1]["id"] != None
    assert response.json()["data"]["transactions"][1]["status"] == "success"
    assert response.json()["data"]["transactions"][1]["transacted_at"] != None
    assert response.json()["data"]["transactions"][1]["type"] == "deposit"
    assert response.json()["data"]["transactions"][1]["amount"] == deposit_amount
    assert response.json()["data"]["transactions"][1]["reference_id"] == reference_id_deposit

def test_disable_wallet_successfully(client):
    data = {"is_disabled":"true"}
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.patch("/api/v1/wallet", data=json.dumps(data), headers=headers)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["wallet"]["id"] != None
    assert response.json()["data"]["wallet"]["owned_by"] == customer_xid
    assert response.json()["data"]["wallet"]["status"] == "disabled"
    assert response.json()["data"]["wallet"]["disabled_at"] != None
    assert response.json()["data"]["wallet"]["balance"] == current_balance

def test_view_wallet_fail_not_enabled(client):
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.get("/api/v1/wallet", headers=headers)

    assert response.status_code == 400
    assert response.json()["status"] == "fail"
    assert response.json()["data"]["error"] == "Wallet disabled"

def test_view_transactions_fail_not_enabled(client):
    token = get_token(client)
    headers = {
        "Authorization" : f"Token {token}"
    }
    response = client.get("/api/v1/wallet/transactions", headers=headers)

    assert response.status_code == 400
    assert response.json()["status"] == "fail"
    assert response.json()["data"]["error"] == "Wallet disabled"





