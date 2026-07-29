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
    raw_limit = request.args.get("limit", "10")

    try:
        limit = int(raw_limit)
    except ValueError:
        logger.warning("Invalid item limit received: %s", raw_limit)

        return jsonify(
            error="Limit must be an integer",
        ), 400

    if not 1 <= limit <= 100:
        logger.warning("Out-of-range item limit received: %s", limit)

        return jsonify(
            error="Limit must be between 1 and 100",
        ), 400

    return jsonify(
        limit=limit,
        message=f"Returning up to {limit} items",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)