# 📦 Complete Boilerplate - Copy All Files Here

## INSTRUCTIONS
Copy each file exactly as shown into your project directory with the correct name and path.

---

## FILE 1: Dockerfile
**Path:** `Dockerfile` (root directory)

```dockerfile
FROM wordpress:6.3-apache

# Install required PHP extensions
RUN apt-get update && apt-get install -y \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy custom content if exists
COPY ./wp-content /var/www/html/wp-content 2>/dev/null || true

# Fix permissions
RUN chown -R www-data:www-data /var/www/html/wp-content

EXPOSE 80
```

---

## FILE 2: render.yaml
**Path:** `render.yaml` (root directory)

```yaml
services:
  # WordPress Web Service
  - type: web
    name: wordpress-demo
    runtime: docker
    region: singapore
    plan: free
    
    dockerfilePath: ./Dockerfile
    branch: main
    
    envVars:
      - key: WORDPRESS_DB_HOST
        sync: false
      - key: WORDPRESS_DB_NAME
        value: wordpress
      - key: WORDPRESS_DB_USER
        sync: false
      - key: WORDPRESS_DB_PASSWORD
        sync: false
      - key: WORDPRESS_TABLE_PREFIX
        value: wp_
      - key: WORDPRESS_DEBUG
        value: "false"
      - key: WORDPRESS_CONFIG_EXTRA
        value: |
          define('WP_HOME', getenv('RENDER_EXTERNAL_URL'));
          define('WP_SITEURL', getenv('RENDER_EXTERNAL_URL'));
    
    disk:
      name: wordpress-data
      mountPath: /var/www/html
      sizeGB: 10
    
    autoDeploy: true

  # MySQL Database
  - type: pserv
    name: wordpress-db-demo
    runtime: mysql
    region: singapore
    plan: free
    
    ipWhitelist:
      - service: wordpress-demo
    
    envVars:
      - key: MYSQL_ROOT_PASSWORD
        sync: false
      - key: MYSQL_DATABASE
        value: wordpress
      - key: MYSQL_USER
        sync: false
      - key: MYSQL_PASSWORD
        sync: false
```

---

## FILE 3: GitHub Actions Workflow
**Path:** `.github/workflows/deploy.yml`

```yaml
name: Deploy to Render

on:
  push:
    branches:
      - main
    paths-ignore:
      - 'README.md'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Validate files
        run: |
          echo "Checking Dockerfile..."
          if [ ! -f Dockerfile ]; then echo "ERROR: Dockerfile missing"; exit 1; fi
          
          echo "Checking render.yaml..."
          if [ ! -f render.yaml ]; then echo "ERROR: render.yaml missing"; exit 1; fi
          
          echo "✅ All files present"
      
      - name: Trigger Render Deploy
        run: |
          if [ -z "${{ secrets.RENDER_DEPLOY_HOOK_URL }}" ]; then
            echo "⚠️ RENDER_DEPLOY_HOOK_URL secret not set. Manual deploy required on first deployment."
            exit 0
          fi
          
          curl --request POST \
            --url ${{ secrets.RENDER_DEPLOY_HOOK_URL }} \
            --header 'Accept: application/json' \
            --fail || echo "Warning: Deploy hook call failed"
```

---

## FILE 4: .gitignore
**Path:** `.gitignore` (root directory)

```
# WordPress core files (managed by Docker)
/wp-admin/
/wp-includes/
wp-*.php
wp-config.php

# Temporary files
*.log
.DS_Store
Thumbs.db

# Environment files
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
```

---

## FILE 5: README.md
**Path:** `README.md` (root directory)

```markdown
# WordPress on Render - Minimal Demo

A copy-paste ready demo project for deploying WordPress on Render with GitHub integration.

## What's Included
- ✅ WordPress Docker setup
- ✅ MySQL database configuration
- ✅ Automatic GitHub to Render deployment
- ✅ Persistent storage for uploads
- ✅ Free tier compatible

## Quick Start

1. **Fork/Clone this repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/wordpress-render-demo.git
   cd wordpress-render-demo
   ```

2. **Run validation script**
   ```bash
   chmod +x validate-setup.sh
   ./validate-setup.sh
   ```

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "WordPress demo setup"
   git push origin main
   ```

4. **Deploy on Render**
   - Visit https://dashboard.render.com
   - Click "New" → "Blueprint"
   - Select this repository
   - Render auto-detects render.yaml
   - Wait 5 minutes for MySQL initialization

5. **Configure Environment Variables**
   - Go to Render → wordpress-demo service
   - Settings → Environment Variables
   - Set WORDPRESS_DB_HOST, DB_USER, DB_PASSWORD

6. **Complete WordPress Setup**
   - Visit your Render service URL
   - Complete WordPress installation wizard

## Testing Auto-Deployment

```bash
# Make a change
echo "# Test" >> README.md

# Commit and push
git add .
git commit -m "Test auto-deploy"
git push origin main

# Watch Render Dashboard for automatic deployment
```

## Directory Structure
```
.
├── Dockerfile              # WordPress container definition
├── render.yaml             # Render infrastructure config
├── .github/
│   └── workflows/
│       └── deploy.yml      # Auto-deploy trigger
├── wp-content/
│   ├── themes/             # Custom themes go here
│   └── plugins/            # Custom plugins go here
└── README.md               # This file
```

## Troubleshooting

**Database Connection Failed**
- Verify WORDPRESS_DB_HOST matches MySQL service hostname
- Wait 5+ minutes for MySQL to fully initialize
- Check Render logs for error details

**WordPress Stuck Installing**
- MySQL service still initializing
- Try refreshing the page
- Check service status in Render Dashboard

**Auto-Deploy Not Working**
- Verify RENDER_DEPLOY_HOOK_URL secret is set in GitHub
- Check GitHub Actions tab for workflow errors
- Test manual deploy from Render Dashboard

## Free Tier Limitations
- 750 hours/month of runtime (24/7 is ~720 hours)
- 1 free database per account
- 15GB/month outbound bandwidth
- Auto-sleep after 15 minutes of inactivity

## Next Steps
- Add custom WordPress theme in wp-content/themes/
- Add custom plugins in wp-content/plugins/
- Configure custom domain in Render settings
- Install security plugins (Jetpack, etc.)
- Setup automated backups

## Support
- Render Docs: https://render.com/docs
- WordPress Docs: https://wordpress.org/support/
- Docker Docs: https://docs.docker.com/
```

---

## SETUP INSTRUCTIONS (Copy-Paste These Commands)

### Step 1: Create GitHub Repository
```bash
# Go to https://github.com/new
# Name: wordpress-render-demo
# Choose public or private
# Click "Create repository"
```

### Step 2: Clone and Setup Locally
```bash
git clone https://github.com/YOUR-USERNAME/wordpress-render-demo.git
cd wordpress-render-demo
```

### Step 3: Create Directory Structure
```bash
mkdir -p .github/workflows
mkdir -p wp-content/themes
mkdir -p wp-content/plugins
```

### Step 4: Copy All Files
Copy each file from above into the correct path with the correct name.

### Step 5: Validate Setup
```bash
chmod +x validate-setup.sh
./validate-setup.sh
```

### Step 6: Push to GitHub
```bash
git add .
git commit -m "Initial WordPress-Render demo setup"
git push origin main
```

### Step 7: Deploy on Render
1. Visit https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Select your repository
4. Name: "WordPress Demo"
5. Click "Apply"
6. Wait 5-10 minutes

### Step 8: Get MySQL Credentials
1. Render Dashboard → wordpress-db-demo service
2. Copy Connection String information
3. Note: Host, User, Password

### Step 9: Set Environment Variables
1. Render Dashboard → wordpress-demo service
2. Settings → Environment
3. Add:
   - WORDPRESS_DB_HOST = (from Step 8)
   - WORDPRESS_DB_USER = (from Step 8)
   - WORDPRESS_DB_PASSWORD = (from Step 8)
4. Save and wait for restart

### Step 10: Complete WordPress Setup
1. Click "wordpress-demo" service URL
2. Complete WordPress installation
3. Login to admin dashboard
4. Done! ✅

### Step 11: Setup Auto-Deploy (Optional)
1. Render Dashboard → wordpress-demo → Settings
2. Copy Deploy Hook URL
3. GitHub → Repository Settings → Secrets and variables
4. Add secret: RENDER_DEPLOY_HOOK_URL
5. Paste URL as value
6. Now pushes to main automatically deploy!

---

## ✅ QUICK CHECKLIST

- [ ] GitHub repository created
- [ ] Files copied to correct paths
- [ ] validate-setup.sh passes all checks
- [ ] Code pushed to GitHub main branch
- [ ] Render Blueprint deployed
- [ ] MySQL database running
- [ ] Environment variables configured
- [ ] WordPress installation complete
- [ ] Can login to admin dashboard
- [ ] Deploy hook setup (optional)
- [ ] Test deployment works

---

## 🆘 COMMON ERRORS & FIXES

### "Cannot connect to database"
**Fix:** 
1. Wait 5+ minutes for MySQL initialization
2. Verify WORDPRESS_DB_HOST is correct
3. Check MySQL service status in Render

### "Dockerfile not found"
**Fix:**
1. Ensure Dockerfile is in root directory
2. Name must be exactly "Dockerfile" (capital D)
3. Push changes to GitHub

### "render.yaml syntax error"
**Fix:**
1. Check YAML indentation (use 2 spaces, not tabs)
2. Verify all quotes are straight quotes (not curly)
3. Use online YAML validator to check

### "GitHub workflow not triggering"
**Fix:**
1. Check .github/workflows/deploy.yml path
2. Branch must be "main" not "master"
3. Check GitHub Actions tab for errors

---

## 📊 EXPECTED RESULTS

After completing setup, you should have:

✅ WordPress running at: https://wordpress-demo-xxxx.onrender.com
✅ Admin dashboard at: https://wordpress-demo-xxxx.onrender.com/wp-admin
✅ MySQL database storing all WordPress data
✅ Persistent disk for uploads/plugins/themes
✅ Auto-deployment on every push to main branch
✅ Free SSL/TLS certificate
✅ All data survives service restarts
```

---

## VALIDATION CHECKLIST FOR EACH FILE

### Dockerfile
- [ ] Contains: `FROM wordpress:6.3-apache`
- [ ] Contains: `RUN apt-get update`
- [ ] Contains: `EXPOSE 80`
- [ ] Name is exactly "Dockerfile" (capital D)
- [ ] Located in root directory

### render.yaml
- [ ] Contains: `services:`
- [ ] Contains: `wordpress-demo` web service
- [ ] Contains: MySQL service (pserv)
- [ ] Contains: `disk:` with `mountPath: /var/www/html`
- [ ] All environment variables marked `sync: false`
- [ ] YAML syntax valid (proper indentation)

### .github/workflows/deploy.yml
- [ ] Contains: `push:` trigger
- [ ] Contains: `main` branch
- [ ] Contains: `Render Deploy` step
- [ ] YAML syntax valid
- [ ] Path must be exactly: `.github/workflows/deploy.yml`

### .gitignore
- [ ] Contains WordPress core directories
- [ ] Contains sensitive files (`.env`)
- [ ] Located in root directory

### README.md
- [ ] Contains setup instructions
- [ ] Contains troubleshooting section
- [ ] Located in root directory
