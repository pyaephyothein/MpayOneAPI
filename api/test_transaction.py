import logging
import uuid
from flask import request
from flask_restful import Resource
from utils.database import create_transaction, update_transaction_status

logger = logging.getLogger(__name__)

class TestTransaction(Resource):
    """Handle Test Transaction API"""
    
    def post(self):
        """
        Create a test transaction
        
        Expected payload:
        {
            "merchant_id": "TEST_MERCHANT",
            "amount": 100.00,
            "currency": "THB",
            "payment_method": "TEST",
            "description": "Test transaction",
            "customer_email": "test@example.com",
            "customer_name": "Test Customer",
            "customer_phone": "0812345678"
        }
        """
        try:
            payload = request.json
            
            # Validate required fields
            required_fields = ['merchant_id', 'amount', 'payment_method']
            for field in required_fields:
                if field not in payload:
                    return {"error": "INVALID_REQUEST", "message": f"Missing required field: {field}"}, 400
            
            # Generate a unique order ID
            order_id = f"TEST-{uuid.uuid4().hex[:8]}"
            
            # Create the transaction
            transaction = create_transaction(
                merchant_id=payload['merchant_id'],
                order_id=order_id,
                payment_method=payload['payment_method'],
                amount=float(payload['amount']),
                currency=payload.get('currency', 'THB'),
                description=payload.get('description'),
                customer_email=payload.get('customer_email'),
                customer_name=payload.get('customer_name'),
                customer_phone=payload.get('customer_phone'),
                payment_channel=payload.get('payment_channel'),
                raw_request=str(payload)
            )
            
            if not transaction:
                return {"error": "SYSTEM_ERROR", "message": "Failed to create transaction"}, 500
            
            # Return success
            return {
                "status": "SUCCESS",
                "order_id": order_id,
                "message": "Test transaction created successfully"
            }, 201
            
        except Exception as e:
            logger.exception("Error creating test transaction")
            return {"error": "SYSTEM_ERROR", "message": str(e)}, 500
            
    def put(self, order_id):
        """
        Update a test transaction status
        
        Expected payload:
        {
            "status": "SUCCESS", // or FAILED, CANCELED
            "payment_id": "PAY123456789" // optional
        }
        """
        try:
            payload = request.json
            
            # Validate required fields
            if 'status' not in payload:
                return {"error": "INVALID_REQUEST", "message": "Missing required field: status"}, 400
            
            # Validate status
            valid_statuses = ['SUCCESS', 'FAILED', 'CANCELED']
            if payload['status'] not in valid_statuses:
                return {"error": "INVALID_REQUEST", "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}, 400
            
            # Update the transaction
            success = update_transaction_status(
                order_id=order_id,
                status=payload['status'],
                payment_id=payload.get('payment_id'),
                raw_response=str(payload)
            )
            
            if not success:
                return {"error": "RESOURCE_NOT_FOUND", "message": f"Transaction not found: {order_id}"}, 404
            
            # Return success
            return {
                "status": "SUCCESS",
                "message": f"Transaction {order_id} updated to {payload['status']}"
            }, 200
            
        except Exception as e:
            logger.exception("Error updating test transaction")
            return {"error": "SYSTEM_ERROR", "message": str(e)}, 500