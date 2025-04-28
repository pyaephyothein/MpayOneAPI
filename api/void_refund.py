import json
import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.signature import verify_signature

logger = logging.getLogger(__name__)

class WebhookHandler(Resource):
    """Handle Webhook Notifications from mPAY ONE"""
    
    def post(self):
        """
        Process webhook notifications from mPAY ONE
        
        Expected payload structure varies by payment type, but commonly includes:
        {
            "merchant_id": "MERCHANT_ID",
            "order_id": "ORDER123",
            "amount": 100.00,
            "currency": "THB",
            "payment_id": "PAY123",
            "status": "SUCCESS",
            "payment_method": "CREDIT_CARD",
            "payment_channel": "VISA",
            "paid_agent": "BANK",
            "paid_channel": "CC",
            "transaction_time": "2024-01-01T12:00:00+07:00",
            "signature": "SIGNATURE"
        }
        """
        try:
            webhook_data = request.get_json()
            
            if not webhook_data:
                logger.error("Empty webhook payload received")
                return jsonify({"status": "error", "message": "No data received"}), 400
            
            logger.info(f"Received webhook: {json.dumps(webhook_data)}")
            
            # Verify signature
            signature = webhook_data.pop('signature', None)
            
            if not signature:
                logger.error("Webhook signature missing")
                return jsonify({"status": "error", "message": "Signature missing"}), 400
            
            # Verify the signature
            if not verify_signature(webhook_data, signature):
                logger.error("Webhook signature verification failed")
                return jsonify({"status": "error", "message": "Invalid signature"}), 401
            
            # Process the webhook based on status
            status = webhook_data.get('status')
            payment_method = webhook_data.get('payment_method')
            order_id = webhook_data.get('order_id')
            
            if not all([status, payment_method, order_id]):
                logger.error("Webhook missing critical fields")
                return jsonify({"status": "error", "message": "Missing required fields"}), 400
            
            # Handle different payment statuses
            if status == 'SUCCESS':
                logger.info(f"Payment successful for order {order_id}")
                # Update your system - payment successful
                # e.g. update_order_status(order_id, 'paid')
                
            elif status == 'PENDING':
                logger.info(f"Payment pending for order {order_id}")
                # Update your system - payment is being processed
                # e.g. update_order_status(order_id, 'pending')
                
            elif status == 'FAILED':
                logger.info(f"Payment failed for order {order_id}")
                # Update your system - payment failed
                # e.g. update_order_status(order_id, 'failed')
                
            elif status == 'AUTHORIZED':
                logger.info(f"Payment authorized for order {order_id}")
                # Update your system - payment authorized but not captured
                # e.g. update_order_status(order_id, 'authorized')
                
            elif status == 'CANCELED':
                logger.info(f"Payment canceled for order {order_id}")
                # Update your system - payment was canceled
                # e.g. update_order_status(order_id, 'canceled')
                
            else:
                logger.warning(f"Unknown payment status: {status} for order {order_id}")
                # Handle unknown status
            
            # Always return 200 OK to acknowledge receipt
            return jsonify({"status": "success", "message": "Webhook received"}), 200
            
        except Exception as e:
            logger.exception("Error processing webhook")
            # Still return 200 to prevent redelivery, but log the error
            return jsonify({"status": "error", "message": str(e)}), 200
