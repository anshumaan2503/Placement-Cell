# 📧 Brevo Email Service Setup Guide

This guide will help you set up Brevo (formerly Sendinblue) as your email service provider for the Placement Cell application.

## 🚀 Why Brevo?

- **Free Tier**: 300 emails/day forever
- **High Deliverability**: Professional email infrastructure
- **API & SMTP**: Multiple sending methods
- **Easy Setup**: Simple configuration process
- **Reliable**: Used by millions of businesses worldwide

## 📋 Step 1: Create Brevo Account

1. Go to [https://www.brevo.com](https://www.brevo.com)
2. Click "Sign up free"
3. Fill in your details:
   - Email address
   - Password
   - Company name (e.g., "IGNTU Placement Cell")
4. Verify your email address
5. Complete the onboarding process

## 🔑 Step 2: Get API Key

1. **Login to Brevo Dashboard**
2. **Go to API Keys**:
   - Click on your profile (top right)
   - Select "SMTP & API"
   - Click "API Keys" tab
3. **Create New API Key**:
   - Click "Generate a new API key"
   - Name: `Placement Cell App`
   - Click "Generate"
4. **Copy the API Key** (save it securely - you won't see it again!)

## 📧 Step 3: Verify Sender Email

1. **Go to Senders & IP**:
   - In dashboard, go to "Senders & IP"
   - Click "Senders" tab
2. **Add Sender**:
   - Click "Add a sender"
   - Email: `placement@yourdomain.com` (or your institutional email)
   - Name: `IGNTU Placement Cell`
   - Click "Save"
3. **Verify Email**:
   - Check your email for verification link
   - Click the verification link

## ⚙️ Step 4: Configure Application

### Option A: Environment Variables (Recommended for Production)

Create/update your `.env` file:

```env
# Brevo Configuration
EMAIL_PROVIDER=brevo
BREVO_API_KEY=your_brevo_api_key_here
SENDER_EMAIL=placement@yourdomain.com
SENDER_NAME=IGNTU Computer Science Placement Cell

# SMTP Fallback (optional)
SMTP_SERVER=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USERNAME=your_brevo_login_email
SMTP_PASSWORD=your_brevo_smtp_password
```

### Option B: Direct Configuration (Development Only)

Update `app.py` directly (not recommended for production):

```python
EMAIL_CONFIG = {
    'provider': 'brevo',
    'brevo_api_key': 'your_brevo_api_key_here',
    'sender_email': 'placement@yourdomain.com',
    'sender_name': 'IGNTU Computer Science Placement Cell',
    # ... other config
}
```

## 🧪 Step 5: Test Email Sending

1. **Start your application**
2. **Generate a student registration link** from admin panel
3. **Check the console output** - you should see:
   ```
   🚀 Attempting to send via Brevo API...
   ✅ Email sent successfully via Brevo API to student@email.com
   ```

## 📊 Step 6: Monitor Email Delivery

1. **Brevo Dashboard**:
   - Go to "Statistics" → "Email"
   - Monitor delivery rates, opens, clicks
2. **Check Logs**:
   - Go to "Logs" to see detailed sending history
   - Troubleshoot any delivery issues

## 🔧 Troubleshooting

### Common Issues:

#### 1. "Invalid API Key" Error
- **Solution**: Double-check your API key in `.env` file
- Make sure there are no extra spaces or quotes

#### 2. "Sender not verified" Error
- **Solution**: Verify your sender email address in Brevo dashboard
- Check spam folder for verification email

#### 3. "Daily limit exceeded"
- **Solution**: You've hit the 300 emails/day free limit
- Upgrade to paid plan or wait until next day

#### 4. Emails going to spam
- **Solution**: 
  - Use a professional sender email (not Gmail/Yahoo)
  - Add SPF/DKIM records to your domain
  - Warm up your sender reputation gradually

### Debug Mode:

To see detailed logs, check your application console output. The app will show:
- Which method is being used (API vs SMTP)
- Success/failure messages
- Fallback to console display if all methods fail

## 🎯 Best Practices

1. **Use Professional Email**: `placement@yourdomain.com` instead of `gmail.com`
2. **Monitor Delivery**: Check Brevo dashboard regularly
3. **Keep API Key Secret**: Never commit API keys to version control
4. **Test Regularly**: Send test emails to verify everything works
5. **Have Fallback**: Configure SMTP as backup method

## 📈 Scaling Up

### Free Tier Limits:
- 300 emails/day
- Unlimited contacts
- Basic support

### Paid Plans Start at $25/month:
- 20,000 emails/month
- No daily sending limit
- Advanced features
- Priority support

## 🔒 Security Notes

- **API Key**: Keep your API key secure and never share it
- **Environment Variables**: Use `.env` file for sensitive data
- **HTTPS**: Always use HTTPS in production
- **Rate Limiting**: Brevo has built-in rate limiting protection

## 📞 Support

- **Brevo Support**: [https://help.brevo.com](https://help.brevo.com)
- **API Documentation**: [https://developers.brevo.com](https://developers.brevo.com)
- **Status Page**: [https://status.brevo.com](https://status.brevo.com)

---

## 🎉 You're All Set!

Once configured, your placement cell application will:
- ✅ Send professional-looking emails
- ✅ Have high delivery rates
- ✅ Provide detailed analytics
- ✅ Scale with your needs

Your students will receive beautiful, professional emails for their registration links and OTPs!