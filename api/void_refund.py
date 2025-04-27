import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, VOID_REFUND_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class VoidRefund(Resource):
    """Handle Void Refund API"""

    def post(self):
        try:
            payload = request.get_json()

            # Validate required fields
            required_fields = ['merchant_id', 'order_id']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400

            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature

            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{VOID_REFUND_ENDPOINT}"
            response = make_request('POST', endpoint, payload)

            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Void refund failed: {response.text}")
                return jsonify({"error": ERROR_CODES["RESOURCE_NOT_FOUND"], "message": response.text}), response.status_code

        except Exception as e:
            logger.exception("Error processing void refund")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
