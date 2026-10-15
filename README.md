# Help Desk Ticketing System (Web App)

A clean, self-hosted web application for managing help desk tickets with remote support requests.

## Features
- Beautiful responsive web interface (Bootstrap)
- Submit tickets with priority and remote support request
- View all tickets
- Admin login to update status and add remote connection details
- Comments on tickets
- SQLite database
- Ready to deploy as a web app

## Default Admin Login
- Password: `admin123`
- Change this via the `ADMIN_PASSWORD` environment variable

## Local Run
```bash
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000

## Deploy Online (so anyone can access it from anywhere)

### Option A: Render.com (Recommended – Free & Easy)

1. Create a free account at [render.com](https://render.com)
2. Push the `helpdesk` folder to a GitHub repository (or use Render’s “Public Git Repository” / upload)
3. In Render, click **New → Web Service**
4. Connect your repo
5. Settings:
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Under **Environment**, add:
   - `ADMIN_PASSWORD` = (choose a strong password)
   - `SECRET_KEY` = (any long random string)
7. Click **Create Web Service**

In a few minutes you’ll get a public URL like `https://your-app-name.onrender.com` that works from any network.

### Option B: Quick Temporary Access with ngrok (for testing)

If you just want to share it right now without deploying:

1. Run the app locally: `python app.py`
2. Install ngrok: https://ngrok.com/download
3. Run: `ngrok http 5000`
4. Share the `https://xxxx.ngrok.io` link ngrok gives you

### Option C: Other Hosts
- Railway.app
- PythonAnywhere
- Fly.io
- Any VPS (DigitalOcean, etc.) using the included Dockerfile

---

## Local Run
