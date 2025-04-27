import os

# mPAY ONE API Endpoints
MPAY_ONE_BASE_URL = os.environ.get("MPAY_ONE_BASE_URL", "https://api-sandbox.mpay.one")

# API Endpoints
CREDIT_CARD_PAYMENT_ENDPOINT = "/api/v4/payment/cc"
CREDIT_CARD_TOKEN_PAYMENT_ENDPOINT = "/api/v4/payment/cc/token"
CREDIT_CARD_TOKEN_INQUIRY_ENDPOINT = "/api/v4/payment/cc/token/inquiry"
CREDIT_CARD_TOKEN_TERMINATE_ENDPOINT = "/api/v4/payment/cc/token/terminate"
CREDIT_CARD_CAPTURE_ENDPOINT = "/api/v4/payment/cc/capture"
CREDIT_CARD_CANCEL_ENDPOINT = "/api/v4/payment/cc/cancel"

CREDIT_CARD_SEAMLESS_PAYMENT_ENDPOINT = "/api/v4/payment/cc/seamless"
CREDIT_CARD_SEAMLESS_REGISTER_ENDPOINT = "/api/v4/payment/cc/seamless/register"
CREDIT_CARD_SEAMLESS_CONFIRM_ENDPOINT = "/api/v4/payment/cc/seamless/confirm"

INSTALLMENT_PLAN_INQUIRY_ENDPOINT = "/api/v4/payment/installment/plan"
INSTALLMENT_PAYMENT_ENDPOINT = "/api/v4/payment/installment"

RLP_PAYMENT_ENDPOINT = "/api/v4/payment/rlp"
RLP_PREAPPROVED_PAYMENT_ENDPOINT = "/api/v4/payment/rlp/preapproved"
RLP_TOKEN_TERMINATE_ENDPOINT = "/api/v4/payment/rlp/terminate"

QR_GENERATE_ENDPOINT = "/api/v4/payment/qr/generate"

INTERNET_BANKING_ENDPOINT = "/api/v4/payment/ib"
REQUEST_TO_PAY_ENDPOINT = "/api/v4/payment/rtp"

PAYMENT_INQUIRY_ENDPOINT = "/api/v4/payment/inquiry"
VOID_REFUND_ENDPOINT = "/api/v4/payment/void-refund"

# API Authentication
MPAY_MERCHANT_ID = os.environ.get("MPAY_MERCHANT_ID", "")
MPAY_SECRET_KEY = os.environ.get("MPAY_SECRET_KEY", "")

# Webhook settings
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-domain.com/api/webhook")

# Payment settings
CURRENCY = "THB"
COUNTRY = "TH"

# Response status codes
STATUS_SUCCESS = "SUCCESS"
STATUS_PENDING = "PENDING"
STATUS_FAILED = "FAILED"
STATUS_AUTHORIZED = "AUTHORIZED"
STATUS_CANCELED = "CANCELED"

# Payment methods
PAYMENT_METHODS = {
    "CREDIT_CARD": "Credit Card",
    "INSTALLMENT": "Installment",
    "QR_PAYMENT": "QR Payment",
    "RLP": "Rabbit Line Pay",
    "INTERNET_BANKING": "Internet Banking",
    "SOF_BIH": "BIH Wallet",
    "SOF_SHOPEEPAY": "ShopeePay",
    "SOF_PAOTANG": "Paotang"
}

# Error codes and messages
ERROR_CODES = {
    "INVALID_REQUEST": "Invalid request parameters",
    "AUTHENTICATION_FAILED": "Authentication failed",
    "SIGNATURE_MISMATCH": "Signature verification failed",
    "PAYMENT_FAILED": "Payment processing failed",
    "RESOURCE_NOT_FOUND": "Requested resource not found",
    "SYSTEM_ERROR": "System error occurred"
}
