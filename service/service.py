import logging
import logging.config
import os
import sys
from typing import List, Union

from flask import Flask, Response, abort, jsonify, request
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest

from urlclassifier.model import load_model

registry = CollectorRegistry()

url_count = Counter(
    "url_count",
    "Number of alerts passed through the service",
    registry=registry,
)
http_codes_count = Counter(
    "http_codes_count",
    "Amount of each http code",
    ["code"],
    registry=registry,
)
verdicts_count = Counter(
    "verdicts_count",
    "Amount of each class",
    ["verdict"],
    registry=registry,
)
time_to_response = Histogram(
    "time_to_response",
    "Time to respone",
    registry=registry,
)


MODEL_PATH = os.getenv("MODEL_PATH", default="model.pkl")
LOG_CONFIG_FILE = os.getenv("LOG_CONFIG_FILE", default="logging.conf")

logging.config.fileConfig(LOG_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)
model = load_model(MODEL_PATH)


def abort_request(message: str, code: int = 400):
    http_codes_count.labels(code).inc()
    logger.error("Request error (%d): %s", code, message)

    response = jsonify(code=code, message=message)
    response.status_code = code
    abort(response)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/metrics")
def metrics():
    return Response(generate_latest(registry), mimetype="text/plain")


@app.route("/predict", methods=["POST"])
@time_to_response.time()
def predict() -> Response:
    data = request.get_json(force=True)
    url_count.inc(len(data))
    try:
        pred_labels = model.predict(data).tolist()
    except (ValueError, KeyError) as err:
        abort_request(str(err), 500)

    for label in pred_labels:
        verdicts_count.labels(label).inc()

    pred_labels = [dict(PedictedGroupId=label) for label in pred_labels]
    pred_labels = pred_labels if isinstance(data, list) else pred_labels[0]
    http_codes_count.labels(200).inc()
    return jsonify(pred_labels)


if __name__ == "__main__":
    try:
        app.run()
    except Exception as err:
        logger.critical(err, exc_info=True)
        sys.exit(1)
