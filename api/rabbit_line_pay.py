import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, RLP_PAYMENT_ENDPOINT, RLP_PREAPPROVED_PAYMENT_ENDPOINT,
    RLP_TOKEN_TERMINATE_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class RabbitLinePayPayment(Resource):
    """Handle Rabbit Line Pay Payment API"""
    
    def post(self):
        """
        Create a Rabbit Line Pay payment order
        
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
            "redirect_url": "https://merchant.com/redirect",
            "backend_url": "https://merchant.com/webhook",
            "settlement": true
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'amount', 'currency', 'redirect_url']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{RLP_PAYMENT_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Rabbit Line Pay payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing Rabbit Line Pay payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class PreApprovedPayment(Resource):
    """Handle Rabbit Line Pay PreApproved Payment API"""
    
    def post(self):
        """
        Create a preapproved payment with Rabbit Line Pay
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,
            "currency": "THB",
            "description": "Payment for order ORDER123",
            "token": "RLP_PREAPPROVED_TOKEN",
            "settlement": true
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'amount', 'currency', 'token']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{RLP_PREAPPROVED_PAYMENT_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Rabbit Line Pay preapproved payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing Rabbit Line Pay preapproved payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class TerminateRLPToken(Resource):
    """Handle Rabbit Line Pay Token Termination API"""
    
    def post(self):
        """
        Terminate a Rabbit Line Pay token
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "token": "RLP_TOKEN"
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'token']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{RLP_TOKEN_TERMINATE_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Rabbit Line Pay token termination failed: {response.text}")
                return jsonify({"error": ERROR_CODES["RESOURCE_NOT_FOUND"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing Rabbit Line Pay token termination")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
