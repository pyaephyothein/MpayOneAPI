// Main JavaScript for mPay ONE API integration

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize payment method selector
    initPaymentMethodSelector();
    
    // Initialize payment form
    initPaymentForm();
});

/**
 * Initialize payment method selector
 */
function initPaymentMethodSelector() {
    const paymentMethodRadios = document.querySelectorAll('input[name="payment_method"]');
    const paymentForms = document.querySelectorAll('.payment-form');
    
    paymentMethodRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Hide all payment forms
            paymentForms.forEach(form => form.classList.add('d-none'));
            
            // Show selected payment form
            const selectedForm = document.getElementById(`${this.value}-form`);
            if (selectedForm) {
                selectedForm.classList.remove('d-none');
            }
        });
    });
}

/**
 * Initialize payment form submission
 */
function initPaymentForm() {
    const paymentForm = document.getElementById('payment-form');
    
    if (paymentForm) {
        paymentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading spinner
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            
            // Get selected payment method
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
            
            try {
                // Build form data based on payment method
                const formData = buildFormData(paymentMethod);
                
                // Call appropriate API endpoint
                const endpoint = getEndpointForPaymentMethod(paymentMethod);
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    handleSuccessResponse(result, paymentMethod);
                } else {
                    handleErrorResponse(result);
                }
            } catch (error) {
                console.error('Payment processing error:', error);
                showErrorMessage('An unexpected error occurred. Please try again.');
            } finally {
                // Restore submit button
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    }
}

/**
 * Build form data based on payment method
 */
function buildFormData(paymentMethod) {
    const formData = {
        merchant_id: document.getElementById('merchant_id').value,
        order_id: document.getElementById('order_id').value,
        amount: parseFloat(document.getElementById('amount').value),
        currency: document.getElementById('currency').value,
        description: document.getElementById('description').value
    };
    
    // Add common customer details if available
    const customerEmail = document.getElementById('customer_email');
    const customerName = document.getElementById('customer_name');
    const customerPhone = document.getElementById('customer_phone');
    
    if (customerEmail && customerEmail.value) formData.customer_email = customerEmail.value;
    if (customerName && customerName.value) formData.customer_name = customerName.value;
    if (customerPhone && customerPhone.value) formData.customer_phone = customerPhone.value;
    
    // Add redirect and backend URLs if available
    const redirectUrl = document.getElementById('redirect_url');
    const backendUrl = document.getElementById('backend_url');
    
    if (redirectUrl && redirectUrl.value) formData.redirect_url = redirectUrl.value;
    if (backendUrl && backendUrl.value) formData.backend_url = backendUrl.value;
    
    // Add method-specific fields
    switch (paymentMethod) {
        case 'credit_card':
            // Credit Card specific fields would be handled by redirect to mPAY ONE payment page
            break;
            
        case 'qr_payment':
            // QR Payment specific fields
            break;
            
        case 'rabbit_line_pay':
            // Rabbit Line Pay specific fields
            break;
            
        case 'installment':
            // Add installment specific fields
            const installmentPlan = document.getElementById('installment_plan');
            const installmentBank = document.getElementById('installment_bank');
            
            if (installmentPlan && installmentPlan.value) formData.installment_plan = installmentPlan.value;
            if (installmentBank && installmentBank.value) formData.installment_bank = installmentBank.value;
            break;
            
        case 'internet_banking':
            // Add internet banking specific fields
            const bankCode = document.getElementById('bank_code');
            if (bankCode && bankCode.value) formData.bank_code = bankCode.value;
            break;
    }
    
    return formData;
}

/**
 * Get API endpoint based on payment method
 */
function getEndpointForPaymentMethod(paymentMethod) {
    switch (paymentMethod) {
        case 'credit_card':
            return '/api/credit-card/payment';
        case 'qr_payment':
            return '/api/qr/generate';
        case 'rabbit_line_pay':
            return '/api/rabbit-line-pay/payment';
        case 'installment':
            return '/api/installment/payment';
        case 'internet_banking':
            return '/api/banking/payment';
        default:
            throw new Error(`Unknown payment method: ${paymentMethod}`);
    }
}

/**
 * Handle successful API response
 */
function handleSuccessResponse(result, paymentMethod) {
    if (result.redirect_url) {
        // Redirect to payment gateway
        window.location.href = result.redirect_url;
    } else if (result.qr_image) {
        // Show QR code
        showQRCode(result.qr_image);
    } else {
        // Show success message
        showSuccessMessage('Payment initiated successfully. Order ID: ' + result.order_id);
    }
}

/**
 * Handle error API response
 */
function handleErrorResponse(result) {
    let errorMessage = 'Payment processing failed.';
    
    if (result.error && result.message) {
        errorMessage = `${result.error}: ${result.message}`;
    } else if (result.error) {
        errorMessage = result.error;
    } else if (result.message) {
        errorMessage = result.message;
    }
    
    showErrorMessage(errorMessage);
}

/**
 * Show QR code in modal
 */
function showQRCode(qrImageData) {
    const modalBody = document.querySelector('#qr-modal .modal-body');
    modalBody.innerHTML = `
        <div class="text-center">
            <img src="${qrImageData}" alt="QR Code" class="img-fluid qr-image">
            <p class="mt-3">Scan this QR code with your banking application to complete the payment</p>
        </div>
    `;
    
    const qrModal = new bootstrap.Modal(document.getElementById('qr-modal'));
    qrModal.show();
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    alertContainer.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Scroll to alert
    alertContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    alertContainer.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Scroll to alert
    alertContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Format currency
 */
function formatCurrency(amount, currency = 'THB') {
    return new Intl.NumberFormat('th-TH', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Payment inquiry function
 */
async function inquirePayment(orderId) {
    try {
        const response = await fetch('/api/payment/inquiry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                merchant_id: document.getElementById('merchant_id').value,
                order_id: orderId
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showPaymentStatus(result);
        } else {
            handleErrorResponse(result);
        }
    } catch (error) {
        console.error('Payment inquiry error:', error);
        showErrorMessage('Failed to inquire payment status. Please try again.');
    }
}

/**
 * Show payment status
 */
function showPaymentStatus(paymentData) {
    const modalBody = document.querySelector('#status-modal .modal-body');
    
    let statusClass = 'text-secondary';
    if (paymentData.status === 'SUCCESS') {
        statusClass = 'text-success';
    } else if (paymentData.status === 'FAILED') {
        statusClass = 'text-danger';
    } else if (paymentData.status === 'AUTHORIZED') {
        statusClass = 'text-info';
    }
    
    modalBody.innerHTML = `
        <div class="payment-status">
            <p><strong>Order ID:</strong> ${paymentData.order_id}</p>
            <p><strong>Amount:</strong> ${formatCurrency(paymentData.amount, paymentData.currency)}</p>
            <p><strong>Status:</strong> <span class="${statusClass}">${paymentData.status}</span></p>
            <p><strong>Payment Method:</strong> ${paymentData.payment_method || '-'}</p>
            <p><strong>Payment Channel:</strong> ${paymentData.payment_channel || '-'}</p>
            <p><strong>Transaction Time:</strong> ${paymentData.transaction_time || '-'}</p>
        </div>
    `;
    
    const statusModal = new bootstrap.Modal(document.getElementById('status-modal'));
    statusModal.show();
}
