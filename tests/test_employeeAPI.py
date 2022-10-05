import json

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
data = {
    'employee_id': '3776m411444236001016886422099360',
    'name': '員工一',
    'sex': 'm',
    'birthday': '1970-01-01',
    'telephone': None,
    'cellphone': None,
    'address': '新北市淡水區',
    'email': None,
    'hired_date': '2022-09-12',
    'salary': 5000,
    'salary_unit': '日'
}
url = '/api/employee/'

def test_get(client):
    response = client.get(url+data['employee_id'], headers=headers)
    response = json.loads(response.data)
    # assert response == ''
    assert response["name"] == data["name"] 
    assert response["sex"] == data["sex"] 
    assert response["birthday"] == data["birthday"] 
    assert response["telephone"] == data["telephone"] 
    assert response["cellphone"] == data["cellphone"] 
    assert response["address"] == data["address"] 
    assert response["email"] == data["email"]

def test_insert(client):
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status == '201 CREATED'