from datetime import datetime

# In-memory data storage since we're removing database functionality
merchants = {}
transactions = {}
card_tokens = {}
webhooks = {}
refund_voids = {}

class Merchant:
    """Merchant model to store merchant information"""
    
    def __init__(self, merchant_id, name, api_key=None, active=True):
        self.id = len(merchants) + 1
        self.merchant_id = merchant_id
        self.name = name
        self.api_key = api_key
        self.active = active
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def __repr__(self):
        return f"<Merchant {self.merchant_id} - {self.name}>"


class Transaction:
    """Transaction model to store payment transactions"""
    
    def __init__(self, order_id, merchant_id, payment_method, amount, currency="THB", 
                 payment_channel=None, description=None, customer_email=None, 
                 customer_name=None, customer_phone=None, raw_request=None):
        self.id = len(transactions) + 1
        self.order_id = order_id
        self.merchant_id = merchant_id
        self.payment_method = payment_method
        self.payment_channel = payment_channel
        self.amount = amount
        self.currency = currency
        self.status = "PENDING"
        self.description = description
        self.customer_email = customer_email
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.payment_id = None
        self.transaction_time = datetime.utcnow()
        self.completed_at = None
        self.raw_request = raw_request
        self.raw_response = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<Transaction {self.order_id} - {self.status}>"


class CardToken:
    """Card token model to store tokenized credit cards"""
    
    def __init__(self, token, merchant_id, card_mask=None, card_type=None, 
                expiry_month=None, expiry_year=None, card_holder_name=None):
        self.id = len(card_tokens) + 1
        self.token = token
        self.merchant_id = merchant_id
        self.card_mask = card_mask  # Masked card number for display (e.g., "411111******1111")
        self.card_type = card_type  # VISA, MASTERCARD, etc.
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.card_holder_name = card_holder_name
        self.is_active = True
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<CardToken {self.token[:10]}... - {self.card_type}>"


class Webhook:
    """Webhook model to store webhook notifications"""
    
    def __init__(self, order_id, event_type, payload, transaction_id=None, 
                signature=None, is_valid=True, processed=False):
        self.id = len(webhooks) + 1
        self.transaction_id = transaction_id
        self.order_id = order_id
        self.event_type = event_type  # payment.success, payment.failed, etc.
        self.payload = payload
        self.signature = signature
        self.is_valid = is_valid
        self.processed = processed
        self.received_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<Webhook {self.id} - {self.event_type}>"


class RefundVoid:
    """Refund/Void model to store refund and void operations"""
    
    def __init__(self, transaction_id, refund_type, amount=None, description=None, raw_request=None):
        self.id = len(refund_voids) + 1
        self.transaction_id = transaction_id
        self.refund_type = refund_type  # REFUND or VOID
        self.amount = amount  # For partial refunds
        self.description = description
        self.status = "PENDING"  # PENDING, SUCCESS, FAILED
        self.payment_id = None
        self.raw_request = raw_request
        self.raw_response = None
        self.created_at = datetime.utcnow()
        self.completed_at = None
    
    def __repr__(self):
        return f"<RefundVoid {self.refund_type} - {self.status}>"