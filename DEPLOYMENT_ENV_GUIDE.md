# 🚀 Production Environment Variables Setup Guide

This guide helps you set up environment variables for production deployment.

## 📋 Required Environment Variables

Copy these exact values to your production hosting platform:

```bash
# Core Application
SECRET_KEY=xmFKeIrNN2O6lEXXlPNizfAtpqLsCd0ytRAqhK0Kx94
MONGODB_URI=mongodb+srv://testuser:testpass123@placement-cluster.twfnkpl.mongodb.net/studetsdb?retryWrites=true&w=majority

# Email Service - Brevo
EMAIL_PROVIDER=brevo
BREVO_API_KEY=your_brevo_api_key_here
SENDER_EMAIL=attechno8@gmail.com
SENDER_NAME=IGNTU Computer Science Placement Cell

# SMTP Fallback (Optional)
SMTP_SERVER=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USERNAME=attechno8@gmail.com
SMTP_PASSWORD=

# Flask Configuration
FLASK_ENV=production
PORT=5000
```

## 🌐 Platform-Specific Instructions

### **Vercel Deployment**

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Select Your Project** or create new one
3. **Settings** → **Environment Variables**
4. **Add each variable**:
   - Name: `EMAIL_PROVIDER`, Value: `brevo`
   - Name: `BREVO_API_KEY`, Value: `your_brevo_api_key_here`
   - Name: `SENDER_EMAIL`, Value: `attechno8@gmail.com`
   - Name: `SENDER_NAME`, Value: `IGNTU Computer Science Placement Cell`
   - (Add all other variables from the list above)

5. **Deploy**: Push to GitHub or redeploy

### **Railway Deployment**

1. **Go to Railway**: https://railway.app/dashboard
2. **New Project** → **Deploy from GitHub repo**
3. **Variables Tab**
4. **Add Variables** (copy from list above)
5. **Deploy**

### **Render Deployment**

1. **Go to Render**: https://render.com/dashboard
2. **New** → **Web Service**
3. **Connect GitHub repo**
4. **Environment Tab**
5. **Add Environment Variables** (copy from list above)
6. **Create Web Service**

### **Heroku Deployment**

1. **Go to Heroku**: https://dashboard.heroku.com/apps
2. **Create New App**
3. **Settings** → **Config Vars**
4. **Reveal Config Vars**
5. **Add each variable** (copy from list above)
6. **Deploy** via GitHub or Heroku CLI

## 🔍 **Verification Steps**

After deployment, verify your setup:

1. **Check Application Logs**:
   - Look for "MongoDB connected successfully!"
   - Look for "Brevo API" messages when sending emails

2. **Test Email Functionality**:
   - Generate a student registration link
   - Check if emails are sent successfully

3. **Monitor Brevo Dashboard**:
   - Go to https://app.brevo.com
   - Check email statistics and delivery

## 🚨 **Common Issues & Solutions**

### **Issue**: "MongoDB connection failed"
**Solution**: Double-check your `MONGODB_URI` is exactly correct

### **Issue**: "Brevo API error"
**Solution**: Verify your `BREVO_API_KEY` is complete and correct

### **Issue**: "Module not found" errors
**Solution**: Make sure `requirements.txt` is in your repo root

### **Issue**: Application won't start
**Solution**: Check that `PORT` environment variable is set

## 🔒 **Security Best Practices**

1. **Never commit `.env` to Git** ✅ (Already protected)
2. **Use different API keys** for development vs production
3. **Regularly rotate secrets** (change API keys periodically)
4. **Monitor access logs** in your hosting platform
5. **Use HTTPS only** in production

## 📞 **Need Help?**

If you encounter issues:

1. **Check platform documentation**:
   - Vercel: https://vercel.com/docs
   - Railway: https://docs.railway.app
   - Render: https://render.com/docs
   - Heroku: https://devcenter.heroku.com

2. **Check application logs** in your hosting platform
3. **Test locally first** to ensure everything works
4. **Verify environment variables** are set correctly

## ✅ **Deployment Checklist**

- [ ] All environment variables added to hosting platform
- [ ] Repository connected to hosting platform
- [ ] Application builds successfully
- [ ] MongoDB connection works
- [ ] Brevo email service works
- [ ] Admin login works (admin/123)
- [ ] Student registration flow works
- [ ] File uploads work
- [ ] Document preview works

Your application should now be fully functional in production! 🎉