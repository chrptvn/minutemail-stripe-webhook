import sys

import requests
from fastapi import FastAPI, status
from typing import Dict
import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI()


@app.post("/v1/stripe_webhook", status_code=status.HTTP_200_OK)
def keycloak_webhook(data: Dict):
    payload = {
        "subscription_id": data['data']['object']['id'],
        "customer_id": data['data']['object']['customer'],
        "product_id": data['data']['object']['items']['data'][0]['plan']['product'],
        "subscription_item_id": data['data']['object']['items']['data'][0]['id'],
    }

    if data['type'] == 'customer.subscription.created':
        requests.post("http://minutemail-subscription-api.minutemail.svc.cluster.local:8080/v1/membership/activate",
                      json=payload,
                      headers={"Content-Type": "application/json"})
    elif data['type'] == 'customer.subscription.deleted':
        requests.post("http://minutemail-subscription-api.minutemail.svc.cluster.local:8080/v1/membership/cancel_premium",
                      json=payload,
                      headers={"Content-Type": "application/json"})
    elif data['type'] == 'customer.subscription.paused':
        requests.post("http://minutemail-subscription-api.minutemail.svc.cluster.local:8080/v1/membership/deactivate",
                      json=payload,
                      headers={"Content-Type": "application/json"})
    elif data['type'] == 'customer.subscription.resumed':
        requests.post("http://minutemail-subscription-api.minutemail.svc.cluster.local:8080/v1/membership/activate",
                      json=payload,
                      headers={"Content-Type": "application/json"})
    elif data['type'] == 'customer.subscription.updated':
        requests.post("http://minutemail-subscription-api.minutemail.svc.cluster.local:8080/v1/membership/update",
                      json=payload,
                      headers={"Content-Type": "application/json"})
    return {"status": "success", "message": "Webhook processed successfully"}
