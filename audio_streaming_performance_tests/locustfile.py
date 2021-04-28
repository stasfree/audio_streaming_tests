import time
from locust import HttpUser, TaskSet, task, between

headers = {
        'Authorization': '',
        'Content-Type': 'application/json',
        'accept': '*/*'
    }

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    def on_start(self):
        with self.client.post("/login", json = {"email": "abcd@gmail.com", "password": "12345"}) as res:
            headers.update({'Authorization': res.headers['Authorization']})
        
    @task
    def hello_world(self):
        self.client.get("/hello")
    
    @task
    def get_audio(self):
        self.client.get("/audio", headers=headers)
        self.client.get("/audio/6522", headers=headers)
        self.client.get("/audio/scan", headers=headers)