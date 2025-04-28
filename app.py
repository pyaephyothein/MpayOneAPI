import os
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_weasyprint import HTML, render_pdf
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mpay_one_secret_key")

# Apply proxy fix for proper URL generation
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize REST API
api = Api(app)

# Import routes after app initialization to avoid circular imports
from api.credit_card import CreditCardPayment, CardTokenization, CardTokenInquiry, TerminateCardToken, CaptureAuthorized, CancelAuthorized
from api.credit_card import CreditCardPaymentSeamless, RegisterCard, PaymentConfirm
from api.qr_payment import GenerateQR
from api.rabbit_line_pay import RabbitLinePayPayment, PreApprovedPayment, TerminateRLPToken
from api.installment import InstallmentPlanInquiry, InstallmentPayment
from api.internet_banking import InternetBankingPayment, RequestToPay
from api.inquiry import PaymentInquiry
from api.void_refund import VoidRefund
from api.webhook import WebhookHandler




# Credit Card Payment
api.add_resource(CreditCardPayment, '/api/credit-card/payment')
api.add_resource(CardTokenization, '/api/credit-card/payment-token')
api.add_resource(CardTokenInquiry, '/api/credit-card/token-inquiry')
api.add_resource(TerminateCardToken, '/api/credit-card/terminate-token')
api.add_resource(CaptureAuthorized, '/api/credit-card/capture')
api.add_resource(CancelAuthorized, '/api/credit-card/cancel')

# Credit Card Payment (Seamless)
api.add_resource(CreditCardPaymentSeamless, '/api/credit-card/seamless/payment')
api.add_resource(RegisterCard, '/api/credit-card/seamless/register')
api.add_resource(PaymentConfirm, '/api/credit-card/seamless/confirm')

# Installment Payment
api.add_resource(InstallmentPlanInquiry, '/api/installment/inquiry-plan')
api.add_resource(InstallmentPayment, '/api/installment/payment')

# Rabbit Line Pay
api.add_resource(RabbitLinePayPayment, '/api/rabbit-line-pay/payment')
api.add_resource(PreApprovedPayment, '/api/rabbit-line-pay/preapproved-payment')
api.add_resource(TerminateRLPToken, '/api/rabbit-line-pay/terminate-token')

# QR Payment
api.add_resource(GenerateQR, '/api/qr/generate')

# Internet/Mobile Banking
api.add_resource(InternetBankingPayment, '/api/banking/payment')
api.add_resource(RequestToPay, '/api/request-to-pay')

# Inquiry
api.add_resource(PaymentInquiry, '/api/payment/inquiry')

# Void & Refund
api.add_resource(VoidRefund, '/api/payment/void-refund')

# Webhook
api.add_resource(WebhookHandler, '/api/webhook')

# Web routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/payment-form')
def payment_form():
    return render_template('payment_form.html')

@app.route('/download-report-pdf')
def download_report_pdf():
    # Generate PDF report
    html = render_template('report_pdf.html', now=datetime.now())
    return render_pdf(HTML(string=html), download_filename="mPAY_ONE_Project_Report.pdf")

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return jsonify({"error": "Internal server error", "message": str(e)}), 500
