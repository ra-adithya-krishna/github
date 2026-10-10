# Razorpay Payment Gateway Setup Guide

## 🚀 Getting Started with Razorpay

### 1. Create Razorpay Account
1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up for a new account or log in
3. Complete your business profile verification

### 2. Get API Keys
1. Navigate to **Settings** → **API Keys**
2. Generate new API keys or use existing ones
3. Copy your **Key ID** and **Key Secret**

### 3. Configure Django Settings
Update your `ev/settings.py` file with your actual Razorpay credentials:

```python
# Razorpay Configuration
RAZORPAY_KEY_ID = 'rzp_test_your_actual_key_id_here'  # Replace with your actual Key ID
RAZORPAY_KEY_SECRET = 'your_actual_key_secret_here'   # Replace with your actual Key Secret
```

### 4. Test Mode vs Live Mode

#### Test Mode (Recommended for Development)
- Use test API keys (start with `rzp_test_`)
- No real money transactions
- Use test card numbers for testing

#### Live Mode (Production)
- Use live API keys (start with `rzp_live_`)
- Real money transactions
- Requires business verification

### 5. Test Card Numbers

For testing payments, use these test card numbers:

| Card Number | CVV | Expiry | Description |
|-------------|-----|--------|-------------|
| 4111 1111 1111 1111 | 123 | Any future date | Visa (Success) |
| 5555 5555 5555 4444 | 123 | Any future date | Mastercard (Success) |
| 4000 0000 0000 0002 | 123 | Any future date | Visa (Failure) |
| 4000 0000 0000 9995 | 123 | Any future date | Visa (Insufficient Funds) |

### 6. Webhook Setup (Optional)

For production, set up webhooks to handle payment events:

1. Go to **Settings** → **Webhooks**
2. Add webhook URL: `https://yourdomain.com/razorpay/webhook/`
3. Select events: `payment.captured`, `payment.failed`
4. Add webhook secret to settings

### 7. Payment Flow

The integrated payment flow works as follows:

1. **User books slot** → Booking data stored in session
2. **Selects Razorpay** → Redirected to Razorpay payment page
3. **Completes payment** → Razorpay processes payment
4. **Payment success** → Booking saved to database
5. **Confirmation** → User sees success page

### 8. Features Included

✅ **Multiple Payment Methods:**
- Credit/Debit Cards
- UPI (Google Pay, PhonePe, etc.)
- Net Banking
- Digital Wallets

✅ **Security Features:**
- SSL encryption
- Payment signature verification
- Secure callback handling

✅ **User Experience:**
- Modern payment interface
- Real-time payment status
- Error handling and retry options

### 9. Troubleshooting

#### Common Issues:

1. **"Invalid API Key" Error**
   - Check your Key ID and Secret in settings
   - Ensure you're using test keys for development

2. **Payment Not Captured**
   - Verify webhook URL is accessible
   - Check callback URL configuration

3. **Signature Verification Failed**
   - Ensure webhook secret is correctly configured
   - Check payment data integrity

### 10. Support

- **Razorpay Documentation:** [https://razorpay.com/docs/](https://razorpay.com/docs/)
- **Razorpay Support:** [https://razorpay.com/support/](https://razorpay.com/support/)

### 11. Demo vs Live Mode

The system includes both:
- **Razorpay Gateway:** Real payment processing
- **Demo Payment:** Fake payment for testing (no real money)

Users can choose between the two options on the payment page.

---

**Note:** Always use test mode during development and switch to live mode only after thorough testing and business verification.
