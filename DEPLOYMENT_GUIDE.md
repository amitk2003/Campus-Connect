# 🚢 Deployment Guide: CampusConnect

This guide provides steps to deploy the CampusConnect application to production.

---

## ☁️ Option 1: Render / Railway (Recommended)

### 1. Backend Deployment (Python/Flask)
1. **Repository**: Connect your GitHub repository to Render or Railway.
2. **Environment Variables**: Add the following from your `.env` file:
   - `MONGO_URI`: Your MongoDB Atlas connection string.
   - `JWT_SECRET_KEY`: A secure random string.
   - `STRIPE_SECRET_KEY`: Your Stripe secret key.
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn app:app` (Ensure `gunicorn` is in `requirements.txt`).

### 2. Frontend Deployment (Vite/React)
1. **Framework**: Choose "Vite" or "React".
2. **Build Command**: `npm run build`
3. **Publish Directory**: `dist`
4. **Environment Variables**:
   - `VITE_API_URL`: The URL of your deployed backend (e.g., `https://api-campusconnect.onrender.com`).

---

## 🐳 Option 2: Docker Deployment

Create a `docker-compose.yml` in the root directory:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - MONGO_URI=${MONGO_URI}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://backend:5000
```

---

## 📋 Pre-Deployment Checklist
- [ ] **MongoDB**: Ensure IP Whitelisting is set to `0.0.0.0/0` in Atlas.
- [ ] **Stripe**: Switch from `sk_test` to `sk_live` keys for real payments.
- [ ] **Admin Account**: Register one admin account first to lock the admin role.
- [ ] **CORS**: Update `flask_cors` in `app.py` to allow your production frontend domain.

---

## 🚀 Post-Deployment
Once deployed, verify:
1. Registration/Login works.
2. Image uploads are working (Consider using AWS S3 for production image storage).
3. The Admin can see the dashboard but cannot post items.
