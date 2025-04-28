import logging
from typing import Optional
from models import Merchant, Transaction, CardToken, Webhook, RefundVoid
from models import merchants, transactions, card_tokens, webhooks, refund_voids

logger = logging.getLogger(__name__)

def get_merchant_by_id(merchant_id: str) -> Optional[Merchant]:
    """
    Get a merchant by their merchant_id
    
    Args:
        merchant_id (str): The merchant identifier
        
    Returns:
        Optional[Merchant]: The merchant or None if not found
    """
    try:
        # Check if we already have this merchant in our in-memory storage
        for merchant_obj in merchants.values():
            if merchant_obj.merchant_id == merchant_id:
                return merchant_obj
        
        # If not found, create a test merchant for dev purposes
        if merchant_id == "TEST_MERCHANT":
            merchant = Merchant(merchant_id="TEST_MERCHANT", name="Test Merchant")
            merchants[merchant.id] = merchant
            return merchant
            
        return None
    except Exception as e:
        logger.error(f"Error retrieving merchant {merchant_id}: {str(e)}")
        return None

def create_transaction(
    merchant_id: str, 
    order_id: str, 
    payment_method: str, 
    amount: float, 
    currency: str = "THB",
    description: str = None,
    customer_email: str = None,
    customer_name: str = None,
    customer_phone: str = None,
    payment_channel: str = None,
    raw_request: str = None
) -> Optional[Transaction]:
    """
    Create a new transaction record
    
    Args:
        merchant_id (str): The merchant identifier
        order_id (str): The order identifier
        payment_method (str): The payment method used
        amount (float): The transaction amount
        currency (str, optional): The currency code. Defaults to "THB".
        description (str, optional): Transaction description. Defaults to None.
        customer_email (str, optional): Customer email address. Defaults to None.
        customer_name (str, optional): Customer name. Defaults to None.
        customer_phone (str, optional): Customer phone number. Defaults to None.
        payment_channel (str, optional): Payment channel. Defaults to None.
        raw_request (str, optional): Raw request data. Defaults to None.
        
    Returns:
        Optional[Transaction]: The created transaction or None if it failed
    """
    try:
        # Get the merchant object
        merchant = get_merchant_by_id(merchant_id)
        if not merchant:
            logger.error(f"Merchant not found: {merchant_id}")
            return None
        
        # Create a new transaction
        transaction = Transaction(
            order_id=order_id,
            merchant_id=merchant.id,
            payment_method=payment_method,
            amount=amount,
            currency=currency,
            payment_channel=payment_channel,
            description=description,
            customer_email=customer_email,
            customer_name=customer_name,
            customer_phone=customer_phone,
            raw_request=raw_request
        )
        
        # Store in our in-memory dict
        transactions[transaction.id] = transaction
        
        return transaction
    
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        return None

def update_transaction_status(order_id: str, status: str, payment_id: str = None, raw_response: str = None) -> bool:
    """
    Update a transaction status
    
    Args:
        order_id (str): The order identifier
        status (str): The new status (PENDING, SUCCESS, FAILED, CANCELED)
        payment_id (str, optional): The payment ID from payment gateway. Defaults to None.
        raw_response (str, optional): Raw response data. Defaults to None.
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Find transaction by order_id
        transaction = None
        for tx in transactions.values():
            if tx.order_id == order_id:
                transaction = tx
                break
                
        if not transaction:
            logger.error(f"Transaction not found for order_id: {order_id}")
            return False
        
        transaction.status = status
        if payment_id:
            transaction.payment_id = payment_id
        if raw_response:
            transaction.raw_response = raw_response
        
        if status in ["SUCCESS", "FAILED", "CANCELED"]:
            from datetime import datetime
            transaction.completed_at = datetime.utcnow()
        
        # Update in our in-memory storage
        transactions[transaction.id] = transaction
        return True
    
    except Exception as e:
        logger.error(f"Error updating transaction: {str(e)}")
        return False

def save_card_token(
    merchant_id: str, 
    token: str, 
    card_mask: str = None, 
    card_type: str = None,
    expiry_month: str = None,
    expiry_year: str = None,
    card_holder_name: str = None
) -> Optional[CardToken]:
    """
    Save a card token
    
    Args:
        merchant_id (str): The merchant identifier
        token (str): The card token
        card_mask (str, optional): Masked card number. Defaults to None.
        card_type (str, optional): Card type (VISA, MASTERCARD, etc.). Defaults to None.
        expiry_month (str, optional): Card expiry month. Defaults to None.
        expiry_year (str, optional): Card expiry year. Defaults to None.
        card_holder_name (str, optional): Cardholder name. Defaults to None.
        
    Returns:
        Optional[CardToken]: The created card token or None if it failed
    """
    try:
        # Get the merchant object
        merchant = get_merchant_by_id(merchant_id)
        if not merchant:
            logger.error(f"Merchant not found: {merchant_id}")
            return None
        
        # Check if token already exists
        existing_token = None
        for token_obj in card_tokens.values():
            if token_obj.token == token:
                existing_token = token_obj
                break
                
        if existing_token:
            logger.info(f"Card token already exists: {token}")
            return existing_token
        
        # Create a new card token
        card_token = CardToken(
            token=token,
            merchant_id=merchant.id,
            card_mask=card_mask,
            card_type=card_type,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            card_holder_name=card_holder_name
        )
        
        # Store in memory
        card_tokens[card_token.id] = card_token
        
        return card_token
    
    except Exception as e:
        logger.error(f"Error saving card token: {str(e)}")
        return None

def record_webhook(
    order_id: str, 
    event_type: str, 
    payload: str, 
    signature: str = None, 
    is_valid: bool = True
) -> Optional[Webhook]:
    """
    Record a webhook notification
    
    Args:
        order_id (str): The order identifier
        event_type (str): The event type (payment.success, payment.failed, etc.)
        payload (str): The webhook payload
        signature (str, optional): The webhook signature. Defaults to None.
        is_valid (bool, optional): Whether the signature is valid. Defaults to True.
        
    Returns:
        Optional[Webhook]: The created webhook record or None if it failed
    """
    try:
        # Get the transaction
        transaction_id = None
        for tx in transactions.values():
            if tx.order_id == order_id:
                transaction_id = tx.id
                break
        
        # Create a new webhook record
        webhook = Webhook(
            order_id=order_id,
            event_type=event_type,
            payload=payload,
            transaction_id=transaction_id,
            signature=signature,
            is_valid=is_valid,
            processed=False
        )
        
        # Store in memory
        webhooks[webhook.id] = webhook
        
        return webhook
    
    except Exception as e:
        logger.error(f"Error recording webhook: {str(e)}")
        return None

def create_refund_void(
    order_id: str, 
    refund_type: str, 
    amount: float = None, 
    description: str = None, 
    raw_request: str = None
) -> Optional[RefundVoid]:
    """
    Create a refund or void record
    
    Args:
        order_id (str): The order identifier
        refund_type (str): REFUND or VOID
        amount (float, optional): The refund amount (for partial refunds). Defaults to None.
        description (str, optional): The refund/void description. Defaults to None.
        raw_request (str, optional): Raw request data. Defaults to None.
        
    Returns:
        Optional[RefundVoid]: The created refund/void record or None if it failed
    """
    try:
        # Get the transaction
        transaction_id = None
        for tx in transactions.values():
            if tx.order_id == order_id:
                transaction_id = tx.id
                break
                
        if not transaction_id:
            logger.error(f"Transaction not found for order_id: {order_id}")
            return None
        
        # Create a new refund/void record
        refund_void = RefundVoid(
            transaction_id=transaction_id,
            refund_type=refund_type,
            amount=amount,
            description=description,
            raw_request=raw_request
        )
        
        # Store in memory
        refund_voids[refund_void.id] = refund_void
        
        return refund_void
    
    except Exception as e:
        logger.error(f"Error creating refund/void: {str(e)}")
        return None