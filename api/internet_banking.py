import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, INTERNET_BANKING_ENDPOINT, REQUEST_TO_PAY_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class InternetBankingPayment(Resource):
    """Handle Internet/Mobile Banking Payment API"""
    
    def post(self):
        """
        Create an Internet/Mobile Banking payment order
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,
            "currency": "THB",
            "description": "Payment for order ORDER123",
            "customer_email": "customer@example.com",
            "customer_name": "John Doe",
            "language": "en",
            "redirect_url": "https://merchant.com/redirect",
            "backend_url": "https://merchant.com/webhook",
            "bank_code": "SCB",
            "settlement": true
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'amount', 'currency', 'redirect_url', 'bank_code']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{INTERNET_BANKING_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Internet banking payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing internet banking payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class RequestToPay(Resource):
    """Handle Request to Pay API"""
    
    def post(self):
        """
        Create a request to pay
        
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
            "sof": "SOF_PAOTANG",
            "settlement": true
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'amount', 'currency', 'sof']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{REQUEST_TO_PAY_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Request to pay failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing request to pay")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
