import logging
from flask import request
from flask_restful import Resource
from models import Merchant
from utils.database import get_merchant_by_id

logger = logging.getLogger(__name__)

class MerchantInfo(Resource):
    """Handle Merchant Info API"""
    
    def get(self, merchant_id):
        """
        Get merchant information
        """
        try:
            merchant = get_merchant_by_id(merchant_id)
            
            if not merchant:
                return {"error": "MERCHANT_NOT_FOUND", "message": f"Merchant not found: {merchant_id}"}, 404
            
            return {
                "merchant_id": merchant.merchant_id,
                "name": merchant.name,
                "active": merchant.active,
                "created_at": merchant.created_at.isoformat() if merchant.created_at else None
            }, 200
            
        except Exception as e:
            logger.exception("Error retrieving merchant info")
            return {"error": "SYSTEM_ERROR", "message": str(e)}, 500