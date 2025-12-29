# Deployment Guide for Render

## Prerequisites
- Git repository with your code
- Render account

## Environment Variables to Set in Render

1. **SECRET_KEY** (Required)
   - Generate a strong secret key: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Set this in Render dashboard under Environment Variables

2. **DATABASE_URL** (Auto-provided by Render)
   - Render automatically provides this when you add a PostgreSQL database
   - The app will automatically convert `postgres://` to `postgresql://` if needed

3. **ADMIN_PASSWORD_HASH** (Optional)
   - Only set if you want to use a pre-hashed password
   - Otherwise, the default password will be used on first login

4. **FLASK_ENV** (Optional)
   - Set to `production` to disable debug mode

## Deployment Steps

1. **Create a PostgreSQL Database in Render**
   - Go to Render Dashboard → New → PostgreSQL
   - Note the Internal Database URL (auto-set as DATABASE_URL)

2. **Create a Web Service**
   - Go to Render Dashboard → New → Web Service
   - Connect your Git repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Environment**: Python 3
     - **Python Version**: 3.11 or 3.12 (auto-detected)

3. **Set Environment Variables**
   - Add SECRET_KEY (required)
   - DATABASE_URL is auto-set if you linked the PostgreSQL database
   - Optionally set FLASK_ENV=production

4. **Deploy**
   - Render will automatically build and deploy your app
   - The database will be initialized on first request

## Important Notes

- **File Uploads**: Uploaded files are stored in `static/uploads/`. On Render's free tier, these files are ephemeral and will be lost on redeploy. Consider using a persistent storage solution (AWS S3, Cloudinary, etc.) for production.

- **Database**: The app will automatically create tables and seed initial data on first run.

- **Admin Access**: Default admin password is `sundeepchakladar2003` (as per README). Change this in production!

## Start Command

```
gunicorn app:app
```

This is already configured in the `Procfile`.

