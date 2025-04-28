import os

# Database connection
DATABASE_URL = os.environ.get("DATABASE_URL")

# API configuration
MPAY_ONE_BASE_URL = "https://api.mpayone.com/v1"
MPAY_SECRET_KEY = os.environ.get("MPAY_SECRET_KEY", "test_secret_key")

# API endpoints
CREDIT_CARD_PAYMENT_ENDPOINT = "/payment/credit-card"
CREDIT_CARD_TOKEN_PAYMENT_ENDPOINT = "/payment/credit-card/token"
CREDIT_CARD_TOKEN_INQUIRY_ENDPOINT = "/inquiry/token"
CREDIT_CARD_TOKEN_TERMINATE_ENDPOINT = "/terminate/token"
CREDIT_CARD_CAPTURE_ENDPOINT = "/payment/capture"
CREDIT_CARD_CANCEL_ENDPOINT = "/payment/cancel"
CREDIT_CARD_SEAMLESS_PAYMENT_ENDPOINT = "/payment/credit-card/seamless"
CREDIT_CARD_SEAMLESS_REGISTER_ENDPOINT = "/payment/credit-card/register"
CREDIT_CARD_SEAMLESS_CONFIRM_ENDPOINT = "/payment/confirm"

# Alternative naming (for potential legacy code)
CARD_TOKENIZATION_ENDPOINT = "/payment/credit-card/token"
CARD_TOKEN_INQUIRY_ENDPOINT = "/inquiry/token"
TERMINATE_CARD_TOKEN_ENDPOINT = "/terminate/token"
CAPTURE_AUTHORIZED_ENDPOINT = "/payment/capture"
CANCEL_AUTHORIZED_ENDPOINT = "/payment/cancel"
CREDIT_CARD_SEAMLESS_ENDPOINT = "/payment/credit-card/seamless"
REGISTER_CARD_ENDPOINT = "/payment/credit-card/register"
PAYMENT_CONFIRM_ENDPOINT = "/payment/confirm"
INSTALLMENT_PLAN_INQUIRY_ENDPOINT = "/inquiry/installment-plan"
INSTALLMENT_PAYMENT_ENDPOINT = "/payment/installment"
RABBIT_LINE_PAY_ENDPOINT = "/payment/rabbit-line-pay"
RLP_PAYMENT_ENDPOINT = "/payment/rabbit-line-pay"
PREAPPROVED_PAYMENT_ENDPOINT = "/payment/preapproved"
RLP_PREAPPROVED_PAYMENT_ENDPOINT = "/payment/preapproved"
TERMINATE_RLP_TOKEN_ENDPOINT = "/terminate/rabbit-line-pay/token"
RLP_TOKEN_TERMINATE_ENDPOINT = "/terminate/rabbit-line-pay/token"
GENERATE_QR_ENDPOINT = "/payment/qr"
QR_GENERATE_ENDPOINT = "/payment/qr"
INTERNET_BANKING_ENDPOINT = "/payment/internet-banking"
REQUEST_TO_PAY_ENDPOINT = "/payment/request-to-pay"
PAYMENT_INQUIRY_ENDPOINT = "/inquiry/payment"
VOID_REFUND_ENDPOINT = "/payment/void-refund"

# Error codes
ERROR_CODES = {
    "INVALID_REQUEST": "INVALID_REQUEST",
    "PAYMENT_FAILED": "PAYMENT_FAILED",
    "SYSTEM_ERROR": "SYSTEM_ERROR",
    "INVALID_SIGNATURE": "INVALID_SIGNATURE",
    "RESOURCE_NOT_FOUND": "RESOURCE_NOT_FOUND"
}