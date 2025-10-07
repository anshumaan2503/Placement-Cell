# 🚀 Production Deployment Guide

## 📋 Required Environment Variables

Set these in your hosting platform dashboard:

```bash
# Core Application
SECRET_KEY=your_secret_key_here
MONGODB_URI=your_mongodb_connection_string

# Email Service - Brevo
EMAIL_PROVIDER=brevo
BREVO_API_KEY=your_brevo_api_key_here
SENDER_EMAIL=your_email@domain.com
SENDER_NAME=Your Organization Name

# Flask Configuration
FLASK_ENV=production
PORT=5000
```

## 🌐 Platform Instructions

### **Vercel**
1. Go to https://vercel.com/dashboard
2. Import your GitHub repository
3. Go to Settings → Environment Variables
4. Add each variable from the list above
5. Deploy

### **Railway**
1. Go to https://railway.app/dashboard
2. New Project → Deploy from GitHub
3. Variables tab → Add variables
4. Deploy

### **Render**
1. Go to https://render.com/dashboard
2. New → Web Service
3. Connect GitHub repo
4. Environment tab → Add variables
5. Create Web Service

## 🔒 Security Notes

- Never commit API keys to Git
- Use your own Brevo API key from https://app.brevo.com
- Keep your MongoDB credentials secure
- Use HTTPS in production

## ✅ Verification

After deployment:
1. Check application logs for "MongoDB connected"
2. Test email functionality
3. Verify admin login works
4. Test student registration flow

Your application should now be live and functional! 🎉