import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, QR_GENERATE_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class GenerateQR(Resource):
    """Handle QR Payment Generation API"""
    
    def post(self):
        """
        Generate a QR code for payment
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,
            "currency": "THB",
            "description": "Payment for order ORDER123",
            "customer_email": "customer@example.com",
            "customer_name": "John Doe",
            "customer_phone": "0812345678",
            "language": "en",
            "backend_url": "https://merchant.com/webhook",
            "reference1": "ref1",
            "reference2": "ref2",
            "reference3": "ref3",
            "settlement": true
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'amount', 'currency']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{QR_GENERATE_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"QR generation failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error generating QR code")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
