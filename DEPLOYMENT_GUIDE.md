# 🚀 Deployment Guide - IGNTU Placement Cell

## 📋 Pre-deployment Checklist

✅ **Files Created:**
- `Procfile` - Tells the platform how to run your app
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Lists all dependencies

## 🌟 **Recommended Platform: Render**

### **Why Render?**
- ✅ Free tier available
- ✅ Easy GitHub integration
- ✅ Automatic HTTPS
- ✅ Environment variables support
- ✅ No credit card required

### **Step-by-Step Deployment on Render:**

#### **1. Prepare Your Code**
```bash
# Make sure all files are committed to Git
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### **2. Set Up MongoDB Atlas (Free)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create free account
3. Create new cluster (free tier)
4. Create database user
5. Get connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

#### **3. Deploy on Render**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** `igntu-placement-cell`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

#### **4. Set Environment Variables**
In Render dashboard, add these environment variables:

```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/studetsdb
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-16-character-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_NAME=IGNTU Computer Science Placement Cell
```

#### **5. Deploy!**
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)
- Your app will be live at: `https://your-app-name.onrender.com`

## 🔧 **Alternative Platforms:**

### **Railway**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo
3. Add same environment variables
4. Deploy automatically

### **Heroku**
1. Install Heroku CLI
2. `heroku create your-app-name`
3. Set environment variables: `heroku config:set SECRET_KEY=your-key`
4. `git push heroku main`

## 📧 **Email Setup for Production**

### **Gmail App Password Setup:**
1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account Settings
3. Security → App Passwords
4. Generate new app password (16 characters)
5. Use this password in `EMAIL_PASSWORD` environment variable

## 🔒 **Security Notes**

- ✅ Never commit real passwords to Git
- ✅ Use environment variables for all secrets
- ✅ Change default secret key
- ✅ Use HTTPS in production (automatic on Render)

## 🧪 **Testing Your Deployment**

1. **Admin Login:** `https://your-app.onrender.com/admin`
2. **Generate OTP:** Create student registration link
3. **Test Email:** Check if emails are sent
4. **Student Registration:** Test the full flow
5. **Export Data:** Test CSV/Excel export

## 🆘 **Troubleshooting**

### **Common Issues:**
- **MongoDB Connection:** Check MONGODB_URI format
- **Email Not Sending:** Verify Gmail App Password
- **App Won't Start:** Check logs in platform dashboard
- **Static Files:** Make sure `static/` folder is committed

### **Logs:**
- **Render:** Dashboard → Logs tab
- **Railway:** Dashboard → Deployments → View Logs
- **Heroku:** `heroku logs --tail`

## 🎯 **Next Steps After Deployment**

1. **Test all functionality**
2. **Share admin URL with placement team**
3. **Test student registration flow**
4. **Monitor email delivery**
5. **Set up regular backups**

---

**🚀 Your placement cell system will be live and ready for testing!**