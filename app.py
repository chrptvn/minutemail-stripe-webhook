import sys

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
    logging.info(f"Received webhook data: {data}")

    return {"status": "success", "message": "Webhook processed successfully"}