import logging
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


@app.get("/")
def index():
    return jsonify(
        service="openshift-maintenance-lab",
        message="Application is running",
    )


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        version=os.getenv("APP_VERSION", "1.0.0"),
    )


@app.get("/divide")
def divide():
    try:
        numerator = float(request.args.get("a", "10"))
        denominator = float(request.args.get("b", "2"))

        if denominator == 0:
            return jsonify(error="Denominator cannot be zero"), 400

        return jsonify(result=numerator / denominator)

    except ValueError:
        logger.exception("Invalid numeric input")
        return jsonify(error="Parameters must be valid numbers"), 400


@app.get("/items")
def items():
    limit = int(request.args.get("limit", "10"))

    return jsonify(
        limit=limit,
        message=f"Returning up to {limit} items",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)