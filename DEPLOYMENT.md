# Nand2Tetris Compiler - Render Deployment Guide

This guide will help you deploy the Nand2Tetris Compiler to Render.

## Prerequisites

- A GitHub account with your code pushed to: https://github.com/josegibson/NANDtoTETRIS.git
- A Render account (free tier works fine)

## Deployment Steps

### 1. Push Your Code to GitHub

Make sure all the configuration files are committed and pushed:

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Create a New Blueprint on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository: `josegibson/NANDtoTETRIS`
4. Render will automatically detect the `render.yaml` file
5. Give your blueprint a name (e.g., "Nand2Tetris Compiler")
6. Click **"Apply"**

### 3. Wait for Deployment

Render will automatically:
- Create two services:
  - `nand-compiler-api` (Flask backend)
  - `nand-compiler-web` (React frontend)
- Install dependencies
- Build both services
- Deploy them

This process takes about 5-10 minutes.

### 4. Access Your Application

Once deployed, you'll get two URLs:
- **Frontend**: `https://nand-compiler-web.onrender.com` (or similar)
- **Backend API**: `https://nand-compiler-api.onrender.com` (or similar)

The frontend will automatically connect to the backend API.

## Configuration Files Created

- **`render.yaml`**: Blueprint configuration for both services
- **`server/runtime.txt`**: Specifies Python 3.13.3
- **`server/requirements.txt`**: Updated with `gunicorn` for production
- **`web/.env.example`**: Example environment variables

## Important Notes

### Free Tier Limitations

- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- 750 hours/month of runtime (shared across all services)

### Environment Variables

The frontend automatically receives the backend URL via the `VITE_API_URL` environment variable, which is set in `render.yaml`.

### CORS Configuration

The backend is configured to accept requests from any origin in development. In production, you can restrict this by setting the `ALLOWED_ORIGINS` environment variable in Render:

1. Go to your backend service settings
2. Add environment variable: `ALLOWED_ORIGINS`
3. Set value to: `https://nand-compiler-web.onrender.com` (your frontend URL)

## Local Development

To run locally:

### Backend
```bash
cd server
pip install -r requirements.txt
python server.py
```

### Frontend
```bash
cd web
npm install
npm run dev
```

## Troubleshooting

### Backend Issues
- Check logs in Render dashboard
- Verify Python version matches `runtime.txt`
- Ensure all dependencies are in `requirements.txt`

### Frontend Issues
- Check that `VITE_API_URL` is set correctly
- Verify build completes successfully
- Check browser console for errors

### CORS Errors
- Ensure backend `ALLOWED_ORIGINS` includes your frontend URL
- Check that both services are running

## Updating Your Deployment

Simply push changes to your GitHub repository:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically detect changes and redeploy both services.

## Custom Domain (Optional)

To use a custom domain:
1. Go to your frontend service settings in Render
2. Click "Custom Domains"
3. Follow the instructions to add your domain
4. Update DNS records as instructed

---

**Need help?** Check the [Render documentation](https://render.com/docs) or open an issue on GitHub.
