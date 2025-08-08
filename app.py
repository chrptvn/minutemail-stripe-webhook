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
    customer_id = data['data']['object']['customer']
    if data['type'] == 'customer.subscription.created':
        payload = {
          "subscription_id": data['data']['object']['id'],
          "customer_id": customer_id,
          "product_id": data['data']['object']['items']['data'][0]['plan']['product']
        }
        logging.info(f"Activating membership {payload}")
        requests.post("http://minutemail-subscription-api.minutemail.svc.cluster.local:8080/v1/membership/activate",
                      json=payload,
                      headers={"Content-Type": "application/json"})
    elif data['type'] == 'customer.subscription.deleted':
        requests.post("http://minutemail-subscription-api.minutemail.svc.cluster.local:8080/v1/membership/deactivate",
                      json={"customer_id": customer_id, "product_id": data['data']['object']['items']['data'][0]['price']['product']},
                      headers={"Content-Type": "application/json"})
        logging.info(f"Deactivated membership for customer_id: {customer_id}")
    return {"status": "success", "message": "Webhook processed successfully"}