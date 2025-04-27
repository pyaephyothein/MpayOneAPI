import json
import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import generate_signature
from utils.http_client import make_request
from config import (
    MPAY_ONE_BASE_URL, CREDIT_CARD_PAYMENT_ENDPOINT, CREDIT_CARD_TOKEN_PAYMENT_ENDPOINT,
    CREDIT_CARD_TOKEN_INQUIRY_ENDPOINT, CREDIT_CARD_TOKEN_TERMINATE_ENDPOINT,
    CREDIT_CARD_CAPTURE_ENDPOINT, CREDIT_CARD_CANCEL_ENDPOINT,
    CREDIT_CARD_SEAMLESS_PAYMENT_ENDPOINT, CREDIT_CARD_SEAMLESS_REGISTER_ENDPOINT,
    CREDIT_CARD_SEAMLESS_CONFIRM_ENDPOINT, ERROR_CODES
)

logger = logging.getLogger(__name__)

class CreditCardPayment(Resource):
    """Handle Credit Card Payment Order API"""
    
    def post(self):
        """
        Create a credit card payment order
        
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
            "capture": true,
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
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_PAYMENT_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Credit card payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing credit card payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class CardTokenization(Resource):
    """Handle Credit Card Payment with Card Tokenization API"""
    
    def post(self):
        """
        Create a payment using tokenized card
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,
            "currency": "THB",
            "description": "Payment for order ORDER123",
            "token": "CARD_TOKEN",
            "capture": true,
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
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_TOKEN_PAYMENT_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Card tokenization payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing card tokenization payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class CardTokenInquiry(Resource):
    """Handle Credit Card Token Inquiry API"""
    
    def post(self):
        """
        Inquiry about a card token
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "token": "CARD_TOKEN"
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
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_TOKEN_INQUIRY_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Card token inquiry failed: {response.text}")
                return jsonify({"error": ERROR_CODES["RESOURCE_NOT_FOUND"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing card token inquiry")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class TerminateCardToken(Resource):
    """Handle Credit Card Token Termination API"""
    
    def post(self):
        """
        Terminate a card token
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "token": "CARD_TOKEN"
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
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_TOKEN_TERMINATE_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Card token termination failed: {response.text}")
                return jsonify({"error": ERROR_CODES["RESOURCE_NOT_FOUND"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing card token termination")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class CaptureAuthorized(Resource):
    """Handle Capture Authorized Payment API"""
    
    def post(self):
        """
        Capture an authorized payment
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,
            "currency": "THB",
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
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_CAPTURE_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Capture authorized payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing capture authorized payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class CancelAuthorized(Resource):
    """Handle Cancel Authorized Payment API"""
    
    def post(self):
        """
        Cancel an authorized payment
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123"
        }
        """
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
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_CANCEL_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Cancel authorized payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing cancel authorized payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class CreditCardPaymentSeamless(Resource):
    """Handle Credit Card Payment Seamless API"""
    
    def post(self):
        """
        Create a credit card payment using seamless integration
        
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
            "backend_url": "https://merchant.com/webhook",
            "capture": true
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
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_SEAMLESS_PAYMENT_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Credit card seamless payment failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing credit card seamless payment")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class RegisterCard(Resource):
    """Handle Credit Card Seamless Register Card API"""
    
    def post(self):
        """
        Register a card for seamless payment
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "card_number": "4111111111111111",
            "card_expiry_month": "12",
            "card_expiry_year": "25",
            "card_holder_name": "John Doe",
            "card_security_code": "123"
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'card_number', 'card_expiry_month', 
                              'card_expiry_year', 'card_holder_name', 'card_security_code']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_SEAMLESS_REGISTER_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Register card failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing register card")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500


class PaymentConfirm(Resource):
    """Handle Credit Card Seamless Payment Confirm API"""
    
    def post(self):
        """
        Confirm a seamless payment
        
        Expected payload:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "payment_code": "PAYMENT_CODE"
        }
        """
        try:
            payload = request.get_json()
            
            # Validate required fields
            required_fields = ['merchant_id', 'order_id', 'payment_code']
            for field in required_fields:
                if field not in payload:
                    return jsonify({"error": ERROR_CODES["INVALID_REQUEST"], "message": f"Missing required field: {field}"}), 400
            
            # Generate signature
            signature = generate_signature(payload)
            payload['signature'] = signature
            
            # Make request to mPAY ONE API
            endpoint = f"{MPAY_ONE_BASE_URL}{CREDIT_CARD_SEAMLESS_CONFIRM_ENDPOINT}"
            response = make_request('POST', endpoint, payload)
            
            if response.status_code == 200:
                return response.json(), 200
            else:
                logger.error(f"Payment confirm failed: {response.text}")
                return jsonify({"error": ERROR_CODES["PAYMENT_FAILED"], "message": response.text}), response.status_code
                
        except Exception as e:
            logger.exception("Error processing payment confirm")
            return jsonify({"error": ERROR_CODES["SYSTEM_ERROR"], "message": str(e)}), 500
