# Pantry Oracle - Deployment Guide

This guide walks you through deploying Pantry Oracle to production using Vercel (frontend) and Railway (backend).

## Prerequisites

- GitHub account
- Vercel account (free tier available)
- Railway account (free tier available) or Render account
- Git installed locally

## Environment Variables

### Frontend (.env.local for development)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5001
NODE_ENV=development
```

### Frontend (.env.production for production)
Set in Vercel dashboard:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NODE_ENV=production
```

### Backend (.env)
Set in Railway/Render dashboard:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5001
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
SECRET_KEY=your-secure-random-secret-key
RATE_LIMIT_PER_HOUR=100
RATE_LIMIT_PER_DAY=1000
LOG_LEVEL=INFO
```

## Step 1: Push Code to GitHub

```bash
cd /Users/kriii/Desktop/s-pantry-oracle
git init
git add .
git commit -m "Initial commit - Pantry Oracle"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pantry-oracle.git
git push -u origin main
```

## Step 2: Deploy Backend to Railway

1. **Sign up/Login to Railway**
   - Go to https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `pantry-oracle` repository

3. **Configure Backend Service**
   - Railway will auto-detect the Python app
   - Set the start command: `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   
4. **Set Environment Variables**
   - Go to Variables tab
   - Add all backend environment variables listed above
   - **Important**: Set `CORS_ORIGINS` to include your Vercel domain (you'll update this after deploying frontend)

5. **Deploy**
   - Railway will automatically deploy
   - Copy the deployment URL (e.g., `https://pantry-oracle-production.up.railway.app`)

## Step 3: Deploy Frontend to Vercel

1. **Sign up/Login to Vercel**
   - Go to https://vercel.com
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New Project"
   - Import your `pantry-oracle` repository

3. **Configure Project**
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

4. **Set Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` with your Railway backend URL
   - Example: `https://pantry-oracle-production.up.railway.app`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Copy your Vercel URL (e.g., `https://pantry-oracle.vercel.app`)

## Step 4: Update CORS Settings

1. **Go back to Railway**
   - Navigate to your backend project
   - Go to Variables tab
   - Update `CORS_ORIGINS` to include your Vercel URL:
     ```
     https://pantry-oracle.vercel.app,https://your-custom-domain.com
     ```
   - Save and redeploy

## Step 5: Test Production Deployment

1. Visit your Vercel URL
2. Test all features:
   - Manual ingredient input
   - OCR upload
   - Recipe search
   - Analytics dashboard

## Optional: Custom Domain

### For Frontend (Vercel)
1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

### For Backend (Railway)
1. Go to your project settings in Railway
2. Navigate to "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed
5. **Remember to update** `CORS_ORIGINS` and frontend `NEXT_PUBLIC_API_URL`

## GitHub Actions CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that automatically:
- Runs tests on pull requests
- Deploys to Vercel on push to main branch

### Required GitHub Secrets

Add these secrets in your GitHub repository settings (Settings → Secrets and variables → Actions):

```
VERCEL_TOKEN - Your Vercel API token
VERCEL_ORG_ID - Your Vercel organization ID
VERCEL_PROJECT_ID - Your Vercel project ID
NEXT_PUBLIC_API_URL - Your backend production URL
```

To get Vercel credentials:
1. Go to https://vercel.com/account/tokens
2. Create a new token
3. Install Vercel CLI: `npm i -g vercel`
4. Run `vercel link` in your frontend directory
5. Find org and project IDs in `.vercel/project.json`

## Troubleshooting

### CORS Errors
- Ensure `CORS_ORIGINS` in backend includes your frontend URL
- Check that URLs don't have trailing slashes
- Verify environment variables are set correctly

### API Connection Errors
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Check backend is running: visit `https://your-backend-url/health`
- Check browser console for specific error messages

### Build Failures
- Check build logs in Vercel/Railway dashboard
- Ensure all dependencies are in package.json/requirements.txt
- Verify Node.js and Python versions are compatible

### OCR Not Working
- OCR requires Tesseract to be installed on the backend server
- Railway/Render may need additional configuration for Tesseract
- Consider using a cloud OCR service (Google Vision, AWS Textract) for production

## Monitoring

### Backend Logs
- View logs in Railway dashboard under "Deployments" → "Logs"

### Frontend Logs
- View logs in Vercel dashboard under "Deployments" → Select deployment → "Logs"

### Analytics
- Use the built-in Analytics dashboard at `/profile` (Analytics tab)
- Consider adding external monitoring (Sentry, LogRocket, etc.)

## Scaling

### Backend
- Railway: Upgrade plan for more resources
- Add more Gunicorn workers: `-w 8` for 8 workers
- Consider Redis for caching instead of in-memory

### Frontend
- Vercel automatically scales
- Enable Edge Functions for better performance
- Add CDN for static assets

## Security Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `FLASK_DEBUG=False` in production
- [ ] Configure rate limiting appropriately
- [ ] Use HTTPS for all connections
- [ ] Keep dependencies updated
- [ ] Enable Vercel security headers (already configured in vercel.json)
- [ ] Review and restrict CORS origins to only trusted domains

## Cost Estimates

### Free Tier Limits
- **Vercel**: 100GB bandwidth, unlimited deployments
- **Railway**: $5 free credit/month, ~500 hours of usage
- **Total**: Free for small to medium traffic

### Paid Plans (if needed)
- **Vercel Pro**: $20/month - More bandwidth and features
- **Railway**: Pay-as-you-go after free credit
- **Estimated**: $20-50/month for moderate traffic

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review deployment logs
3. Check GitHub Issues
4. Contact support for your hosting platform
