from locust import FastHttpUser, task, between
import random


class Load(FastHttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def predict(self):
        payload = {
            "feature_1": random.uniform(-5, 5),
            "feature_2": random.uniform(-5, 5),
        }
        self.client.post("/predict", json=payload)
