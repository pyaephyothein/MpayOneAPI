import hashlib
import hmac
import logging
import json
from config import MPAY_SECRET_KEY

logger = logging.getLogger(__name__)

def generate_signature(data):
    """
    Generate HMAC signature for the request payload
    
    Args:
        data (dict): Payload data to sign
        
    Returns:
        str: The hexadecimal signature string
    """
    try:
        # Sort the payload keys alphabetically
        sorted_data = {k: data[k] for k in sorted(data.keys())}
        
        # Convert payload to JSON string
        payload_string = json.dumps(sorted_data, separators=(',', ':'))
        
        # Create HMAC with SHA-256
        signature = hmac.new(
            MPAY_SECRET_KEY.encode('utf-8'),
            payload_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        logger.debug(f"Generated signature: {signature} for payload: {payload_string}")
        return signature
    
    except Exception as e:
        logger.exception(f"Error generating signature: {str(e)}")
        raise


def verify_signature(data, received_signature):
    """
    Verify HMAC signature from mPAY ONE webhook
    
    Args:
        data (dict): Payload data to verify
        received_signature (str): Signature received from mPAY ONE
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Calculate expected signature
        expected_signature = generate_signature(data)
        
        # Compare with received signature
        is_valid = hmac.compare_digest(expected_signature, received_signature)
        
        if not is_valid:
            logger.warning(
                f"Signature verification failed. Expected: {expected_signature}, Received: {received_signature}"
            )
        
        return is_valid
    
    except Exception as e:
        logger.exception(f"Error verifying signature: {str(e)}")
        return False
