from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from datetime import datetime
import logging
import os
import uuid

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
APP_NAME = "mock-ekyc-api"
APP_VERSION = "v2"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(APP_NAME)

# -----------------------------
# Prometheus Metrics
# -----------------------------
metrics = PrometheusMetrics(app)
metrics.info(
    "app_info",
    "Application info",
    version=APP_VERSION
)

# -----------------------------
# In-memory Mock Database
# -----------------------------
customers = {}

# -----------------------------
# Root Endpoint
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "status": "running"
    })

# -----------------------------
# Health Endpoint
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

# -----------------------------
# Readiness Endpoint
# -----------------------------
@app.route("/ready", methods=["GET"])
def readiness():
    return jsonify({
        "status": "ready"
    }), 200

# -----------------------------
# Create Customer eKYC
# -----------------------------
@app.route("/api/v1/customers", methods=["POST"])
def create_customer():

    data = request.get_json()

    required_fields = [
        "full_name",
        "aadhaar_number",
        "pan_number"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    customer_id = str(uuid.uuid4())

    customer = {
        "customer_id": customer_id,
        "full_name": data["full_name"],
        "aadhaar_number": data["aadhaar_number"],
        "pan_number": data["pan_number"],
        "kyc_status": "VERIFIED",
        "created_at": datetime.utcnow().isoformat()
    }

    customers[customer_id] = customer

    logger.info(f"Customer created: {customer_id}")

    return jsonify(customer), 201

# -----------------------------
# Get Customer
# -----------------------------
@app.route("/api/v1/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):

    customer = customers.get(customer_id)

    if not customer:
        return jsonify({
            "error": "Customer not found"
        }), 404

    return jsonify(customer), 200

# -----------------------------
# Metrics Endpoint
# -----------------------------
@app.route("/metrics")
def metrics_endpoint():
    return metrics.do_not_track()

# -----------------------------
# Global Error Handler
# -----------------------------
@app.errorhandler(Exception)
def handle_exception(error):

    logger.error(str(error))

    return jsonify({
        "error": "Internal server error"
    }), 500

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    logger.info(f"Starting {APP_NAME}")

    app.run(
        host="0.0.0.0",
        port=5000
    )