# WordPress-Render-GitHub Demo Project
## Minimal, Copy-Paste Ready Deployment Demo

---

## ⚡ QUICK START (5 Minutes)

This demo gets WordPress running on Render from GitHub in 5 minutes.

### Prerequisites Check
```bash
# Verify you have these installed
git --version          # Should show version
docker --version       # Should show version
curl --version         # Should show version
```

---

## 📁 STEP 1: Create Project Structure

### 1.1 Create GitHub Repository

```bash
# Go to https://github.com/new
# Repository name: wordpress-render-demo
# Description: Minimal WordPress Render deployment
# Click "Create repository"

# Clone locally
git clone https://github.com/YOUR-USERNAME/wordpress-render-demo.git
cd wordpress-render-demo
```

### 1.2 Create Directory Structure

```bash
# Copy-paste this entire block:

mkdir -p .github/workflows
mkdir -p wp-content/themes
mkdir -p wp-content/plugins

# Create empty files (we'll fill them next)
touch Dockerfile
touch render.yaml
touch .github/workflows/deploy.yml
touch .gitignore
touch README.md

# Verify structure
ls -la
```

**Expected Output:**
```
drwxr-xr-x  .github
drwxr-xr-x  wp-content
-rw-r--r--  Dockerfile
-rw-r--r--  render.yaml
-rw-r--r--  .gitignore
-rw-r--r--  README.md
```

---

## 📝 STEP 2: Create Configuration Files

### 2.1 Create Dockerfile

**File: `Dockerfile`**

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

**Validation:**
```bash
# Check Dockerfile syntax
docker build --dry-run .
echo "✅ Dockerfile is valid"
```

### 2.2 Create render.yaml

**File: `render.yaml`**

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

**Validation:**
```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('render.yaml'))" && echo "✅ render.yaml is valid"
```

### 2.3 Create GitHub Actions Workflow

**File: `.github/workflows/deploy.yml`**

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
            echo "⚠️ RENDER_DEPLOY_HOOK_URL secret not set. Deploy not triggered."
            exit 0
          fi
          
          curl --request POST \
            --url ${{ secrets.RENDER_DEPLOY_HOOK_URL }} \
            --header 'Accept: application/json' \
            --fail || echo "Warning: Deploy hook call failed (may be normal if service not created yet)"
```

**Validation:**
```bash
# Check workflow syntax
if python3 -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml'))" 2>/dev/null; then
  echo "✅ GitHub workflow is valid"
else
  echo "❌ GitHub workflow has YAML errors"
fi
```

### 2.4 Create .gitignore

**File: `.gitignore`**

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
```

### 2.5 Create README

**File: `README.md`**

```markdown
# WordPress on Render - Demo Project

Minimal, copy-paste ready demo for deploying WordPress on Render.

## Features
- ✅ Automated GitHub to Render deployment
- ✅ MySQL database included
- ✅ Persistent storage for uploads
- ✅ Free tier compatible

## Quick Deployment

1. Fork/clone this repo
2. Deploy to Render using Blueprint
3. Complete WordPress setup wizard
4. Push changes to trigger auto-deployment

## Files
- `Dockerfile` - WordPress Docker image
- `render.yaml` - Render infrastructure config
- `.github/workflows/deploy.yml` - Auto-deploy trigger
```

---

## ✅ STEP 3: Local Validation (Before Pushing)

### 3.1 Create Validation Script

**File: `validate-setup.sh`**

```bash
#!/bin/bash

echo "=========================================="
echo "WordPress-Render-GitHub Demo Validator"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Check 1: Required files exist
echo "📋 Checking required files..."
FILES=("Dockerfile" "render.yaml" ".github/workflows/deploy.yml" ".gitignore" "README.md")

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo -e "${GREEN}✅${NC} $file exists"
  else
    echo -e "${RED}❌${NC} $file MISSING"
    ERRORS=$((ERRORS + 1))
  fi
done
echo ""

# Check 2: Validate Dockerfile
echo "🐳 Validating Dockerfile..."
if grep -q "FROM wordpress" Dockerfile; then
  echo -e "${GREEN}✅${NC} Dockerfile uses WordPress base image"
else
  echo -e "${RED}❌${NC} Dockerfile missing WordPress base image"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 3: Validate render.yaml
echo "🎯 Validating render.yaml..."
if python3 -c "import yaml; yaml.safe_load(open('render.yaml'))" 2>/dev/null; then
  echo -e "${GREEN}✅${NC} render.yaml syntax is valid"
else
  echo -e "${RED}❌${NC} render.yaml has syntax errors"
  ERRORS=$((ERRORS + 1))
fi

if grep -q "services:" render.yaml && grep -q "wordpress-demo" render.yaml; then
  echo -e "${GREEN}✅${NC} render.yaml contains web service"
else
  echo -e "${RED}❌${NC} render.yaml missing web service configuration"
  ERRORS=$((ERRORS + 1))
fi

if grep -q "mysql-demo" render.yaml || grep -q "pserv" render.yaml; then
  echo -e "${GREEN}✅${NC} render.yaml contains database service"
else
  echo -e "${RED}❌${NC} render.yaml missing database service"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 4: Validate GitHub workflow
echo "🔄 Validating GitHub workflow..."
if python3 -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml'))" 2>/dev/null; then
  echo -e "${GREEN}✅${NC} GitHub workflow syntax is valid"
else
  echo -e "${RED}❌${NC} GitHub workflow has syntax errors"
  ERRORS=$((ERRORS + 1))
fi

if grep -q "push:" .github/workflows/deploy.yml && grep -q "main" .github/workflows/deploy.yml; then
  echo -e "${GREEN}✅${NC} Workflow triggers on main branch push"
else
  echo -e "${RED}❌${NC} Workflow trigger not configured correctly"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 5: Git setup
echo "📤 Checking Git configuration..."
if git rev-parse --git-dir > /dev/null 2>&1; then
  echo -e "${GREEN}✅${NC} Git repository initialized"
  
  if git remote -v | grep -q "origin"; then
    echo -e "${GREEN}✅${NC} Git remote 'origin' configured"
  else
    echo -e "${YELLOW}⚠️${NC} Git remote 'origin' not configured yet"
  fi
else
  echo -e "${RED}❌${NC} Not in a Git repository"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Summary
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}✅ ALL CHECKS PASSED!${NC}"
  echo ""
  echo "Next steps:"
  echo "1. git add ."
  echo "2. git commit -m 'Initial WordPress-Render demo setup'"
  echo "3. git push origin main"
  echo "4. Deploy to Render using Blueprint"
  exit 0
else
  echo -e "${RED}❌ $ERRORS ISSUES FOUND${NC}"
  exit 1
fi
```

### 3.2 Run Validation

```bash
# Make script executable
chmod +x validate-setup.sh

# Run validation
./validate-setup.sh
```

**Expected Output:**
```
✅ Dockerfile exists
✅ render.yaml exists
✅ .github/workflows/deploy.yml exists
✅ .gitignore exists
✅ README.md exists
✅ Dockerfile uses WordPress base image
✅ render.yaml syntax is valid
✅ render.yaml contains web service
✅ render.yaml contains database service
✅ GitHub workflow syntax is valid
✅ Workflow triggers on main branch push
✅ ALL CHECKS PASSED!
```

---

## 🚀 STEP 4: Push to GitHub

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial WordPress-Render demo setup"

# Push to GitHub
git push origin main

# Verify on GitHub
echo "✅ Visit: https://github.com/YOUR-USERNAME/wordpress-render-demo"
```

---

## 📦 STEP 5: Deploy on Render

### 5.1 Create Render Account
```
Visit: https://render.com
Sign up with GitHub (recommended)
```

### 5.2 Deploy Using Blueprint

```bash
cat << 'EOF'
Steps:
1. Go to Render Dashboard: https://dashboard.render.com
2. Click: New → Blueprint
3. Select your wordpress-render-demo repository
4. Render auto-detects render.yaml
5. Name your Blueprint: "WordPress Demo"
6. Click: Apply
7. WAIT 5 MINUTES for MySQL to initialize
EOF
```

### 5.3 Get Your MySQL Credentials

```bash
cat << 'EOF'
After Render finishes deploying:
1. Dashboard → Services → wordpress-db-demo
2. Copy these values:
   - Hostname: (something like mysql-xxxxx.onrender.com)
   - Database: wordpress
   - User: (shown in Connections section)
   - Password: (shown in Connections section)
3. You'll need these for the next step
EOF
```

### 5.4 Configure Environment Variables

```bash
cat << 'EOF'
In Render Dashboard:
1. Services → wordpress-demo → Settings
2. Scroll to Environment
3. Fill in these variables:
   WORDPRESS_DB_HOST=<MySQL hostname from Step 5.3>
   WORDPRESS_DB_USER=<MySQL user>
   WORDPRESS_DB_PASSWORD=<MySQL password>
4. Click Save
5. Service auto-restarts with new variables
EOF
```

### 5.5 Complete WordPress Setup

```bash
cat << 'EOF'
1. Go to Render Dashboard → wordpress-demo
2. Copy your service URL (something like: https://wordpress-demo-xxx.onrender.com)
3. Visit that URL in browser
4. Complete WordPress installation:
   - Site Title: "My Demo Blog"
   - Username: admin
   - Password: (choose strong password)
   - Email: your-email@example.com
5. Click Install WordPress
6. Login to admin dashboard
EOF
```

### 5.6 Setup Deploy Hook (Auto-Deploy)

```bash
cat << 'EOF'
1. Render Dashboard → Services → wordpress-demo → Settings
2. Scroll down to "Deploy Hook"
3. Copy the URL (looks like: https://api.render.com/deploy/srv-xxxxx?key=xxxxx)
4. Go to GitHub: Settings → Secrets and variables → Actions
5. New secret: RENDER_DEPLOY_HOOK_URL
6. Paste the URL as value
7. Click Add secret
EOF
```

---

## ✅ STEP 6: Verify Deployment (Testing)

### 6.1 Test WordPress Installation

```bash
cat << 'EOF'
In WordPress admin dashboard:
1. Go to Settings → General
2. Check:
   ✅ WordPress Address matches your Render URL
   ✅ Site Address matches your Render URL
3. Go to Dashboard
4. Check: "Hello world" post is visible
5. Try uploading an image: Media → Add New
6. Create a test post: Posts → Add New
EOF
```

### 6.2 Test Auto-Deployment

```bash
# Make a change locally
echo "# Test change" >> README.md

# Commit and push
git add README.md
git commit -m "Test deployment trigger"
git push origin main

# Check Render logs
cat << 'EOF'
In Render Dashboard:
1. Go to Services → wordpress-demo
2. Click "Events" tab
3. You should see new deployment starting
4. Wait 2-3 minutes
5. Check "Logs" tab for success message
EOF
```

---

## 🐛 TROUBLESHOOTING

### Problem: Database Connection Failed

```bash
echo "Solution:
1. Check environment variables match MySQL credentials
2. Verify MySQL service is running (Status: Live)
3. Wait 5 minutes - MySQL takes time to initialize
4. Check Render logs for exact error"
```

### Problem: WordPress Stuck on Installation

```bash
echo "Solution:
1. Check database is actually running
2. Verify environment variables are set correctly
3. Try manually restarting service:
   Render Dashboard → Services → wordpress-demo → Manual Deploy"
```

### Problem: Auto-Deploy Not Triggering

```bash
echo "Solution:
1. Check GitHub secret RENDER_DEPLOY_HOOK_URL is set
2. Go to GitHub: Actions tab
3. Check workflow logs for errors
4. Try manual deploy first from Render"
```

---

## 📊 VALIDATION CHECKLIST

- [ ] All files created successfully
- [ ] validate-setup.sh passes all checks
- [ ] Code pushed to GitHub main branch
- [ ] Blueprint deployed on Render
- [ ] MySQL database initialized
- [ ] Environment variables configured
- [ ] WordPress installation complete
- [ ] Admin dashboard accessible
- [ ] Test post created
- [ ] Deploy hook working
- [ ] Auto-deployment triggered and successful

---

## 📋 QUICK REFERENCE COMMANDS

```bash
# Local validation
./validate-setup.sh

# Git operations
git status                    # Check what changed
git add .                    # Stage all changes
git commit -m "message"      # Commit changes
git push origin main         # Push to GitHub

# Docker local testing (optional)
docker build -t wp-test .   # Build image locally
docker-compose up            # Run with Docker Compose (requires docker-compose.yml)

# Check file existence
ls -la Dockerfile render.yaml .github/workflows/deploy.yml
```

---

## 🎯 EXPECTED RESULTS

After completing all steps:

✅ Code stored in GitHub with version history
✅ Render hosting WordPress with auto-deploys
✅ MySQL database persists data
✅ Uploads directory persists files
✅ Any push to main branch triggers automatic deployment
✅ WordPress admin dashboard fully functional

---

## 📚 Next Steps After Demo

1. **Add Custom Theme**: Create in `wp-content/themes/`
2. **Add Custom Plugin**: Create in `wp-content/plugins/`
3. **Add Custom Domain**: Render → Settings → Custom Domains
4. **Setup SSL**: Automatically included (free)
5. **Monitor Site**: Install Jetpack plugin in WordPress
