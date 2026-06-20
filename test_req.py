import requests
resp = requests.post('http://127.0.0.1:8000/api/users/', json={
    'username': 'testuser2',
    'email': 'test@test.com',
    'password': 'testpassword123',
    'role': 'client'
})
print("STATUS:", resp.status_code)
print("BODY:", resp.text)
