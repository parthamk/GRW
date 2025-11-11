
# Create an interactive step-by-step guide
step_by_step_guide = """
# 🎯 WORDPRESS-RENDER-GITHUB DEMO - STEP-BY-STEP GUIDE

## This guide will take you through the ENTIRE process in order
Follow each step exactly. Do NOT skip steps.

---

# PHASE 1: LOCAL SETUP (15 minutes)

## STEP 1: Create GitHub Repository
**Time: 2 minutes**

[ ] Go to: https://github.com/new
[ ] Repository name: wordpress-render-demo
[ ] Description: Minimal WordPress Render deployment demo
[ ] Choose: Public (easier to share)
[ ] Click: "Create repository"
[ ] Copy the HTTPS clone URL (looks like: https://github.com/YOUR-USERNAME/wordpress-render-demo.git)

**Expected Result:**
- New empty repository on GitHub
- Clone URL copied to clipboard

---

## STEP 2: Clone Repository Locally
**Time: 1 minute**

Open terminal/command prompt and run:

```bash
# Replace with YOUR actual clone URL
git clone https://github.com/YOUR-USERNAME/wordpress-render-demo.git

# Navigate into project
cd wordpress-render-demo

# Verify you're in the right place
pwd
# Should show: .../wordpress-render-demo
```

**Expected Result:**
- New directory called wordpress-render-demo
- Files in terminal show you're inside it
- Can see .git folder (hidden file)

---

## STEP 3: Create Directory Structure
**Time: 2 minutes**

Copy-paste this ENTIRE block into terminal:

```bash
# Create directories
mkdir -p .github/workflows
mkdir -p wp-content/themes
mkdir -p wp-content/plugins

# Create empty files
touch Dockerfile
touch render.yaml
touch .github/workflows/deploy.yml
touch .gitignore
touch README.md

# Verify structure
echo "Checking structure..."
ls -la
echo ""
echo "Total files created:"
find . -type f | wc -l
```

**Expected Output:**
```
.github/
wp-content/
Dockerfile
render.yaml
.gitignore
README.md
```

---

## STEP 4: Create Dockerfile
**Time: 2 minutes**

Using a text editor, open file: `Dockerfile` (in root directory)

Copy and paste EXACTLY:

```dockerfile
FROM wordpress:6.3-apache

# Install required PHP extensions
RUN apt-get update && apt-get install -y \\
    mysql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy custom content if exists
COPY ./wp-content /var/www/html/wp-content 2>/dev/null || true

# Fix permissions
RUN chown -R www-data:www-data /var/www/html/wp-content

EXPOSE 80
```

[ ] File created and saved
[ ] No extra spaces or modifications

---

## STEP 5: Create render.yaml
**Time: 3 minutes**

Open file: `render.yaml` (in root directory)

Copy and paste EXACTLY (watch indentation carefully):

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

[ ] File created and saved
[ ] Indentation looks correct (2 spaces per level)

---

## STEP 6: Create GitHub Workflow
**Time: 2 minutes**

Open file: `.github/workflows/deploy.yml`

Copy and paste EXACTLY:

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
            echo "⚠️ RENDER_DEPLOY_HOOK_URL secret not set"
            exit 0
          fi
          
          curl --request POST \\
            --url ${{ secrets.RENDER_DEPLOY_HOOK_URL }} \\
            --header 'Accept: application/json'
```

[ ] File created and saved
[ ] All quotes are straight quotes (not curly)

---

## STEP 7: Create .gitignore
**Time: 1 minute**

Open file: `.gitignore`

Copy and paste:

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

[ ] File created and saved

---

## STEP 8: Create README
**Time: 1 minute**

Open file: `README.md`

Copy and paste:

```markdown
# WordPress on Render - Demo

Minimal demo for deploying WordPress on Render with GitHub integration.

## Quick Start

1. Clone this repo
2. Deploy to Render using Blueprint
3. Complete WordPress setup wizard
4. Push changes to trigger auto-deployment

## Features
- ✅ WordPress running on Render
- ✅ MySQL database included
- ✅ Auto-deploy from GitHub
- ✅ Free tier compatible
```

[ ] File created and saved

---

## STEP 9: Validate Local Setup
**Time: 2 minutes**

In terminal, run:

```bash
# Go to project root
cd wordpress-render-demo

# Check all files exist
echo "Checking files..."
ls -la Dockerfile render.yaml .github/workflows/deploy.yml .gitignore README.md

# Validate YAML syntax
python3 << 'EOF'
import yaml
try:
    with open('render.yaml') as f:
        yaml.safe_load(f)
    print("✅ render.yaml syntax is valid")
except Exception as e:
    print(f"❌ render.yaml error: {e}")

try:
    with open('.github/workflows/deploy.yml') as f:
        yaml.safe_load(f)
    print("✅ deploy.yml syntax is valid")
except Exception as e:
    print(f"❌ deploy.yml error: {e}")
EOF
```

**Expected Output:**
```
✅ render.yaml syntax is valid
✅ deploy.yml syntax is valid
```

If you get errors:
1. Check indentation (use 2 spaces, not tabs)
2. Check quotes (straight quotes only)
3. Verify no extra spaces at end of lines

---

## STEP 10: Commit and Push to GitHub
**Time: 2 minutes**

In terminal:

```bash
# Check what changed
git status

# Should show all files as "Untracked files"

# Add all files
git add .

# Commit
git commit -m "Initial WordPress-Render demo setup"

# Push to GitHub
git push origin main

# Verify
echo "✅ Code pushed to GitHub!"
```

[ ] All files appear as "new file" changes
[ ] Push completes without errors
[ ] No "Permission denied" errors

**Verify on GitHub:**
1. Go to: https://github.com/YOUR-USERNAME/wordpress-render-demo
2. Should see all files listed
3. Should see "Initial WordPress-Render demo setup" commit message

---

# PHASE 2: RENDER DEPLOYMENT (15 minutes)

## STEP 11: Create Render Account
**Time: 2 minutes**

[ ] Go to: https://render.com
[ ] Click: "Get Started" or "Sign Up"
[ ] Choose: "Sign up with GitHub" (easiest)
[ ] Grant access to your GitHub account
[ ] Verify email (check inbox)

**Expected Result:**
- Render Dashboard shows empty (no services yet)
- Can see GitHub connected

---

## STEP 12: Deploy Using Blueprint
**Time: 5 minutes**

In Render Dashboard:

[ ] Click: "New +" button (top left)
[ ] Select: "Blueprint"
[ ] Select your repository: wordpress-render-demo
[ ] Wait for page to load...

Render will auto-detect render.yaml. You'll see:
- 2 services listed:
  1. wordpress-demo (web)
  2. wordpress-db-demo (MySQL)

[ ] Name your Blueprint: "WordPress Demo"
[ ] Click: "Apply"

Now WAIT 5-10 MINUTES while Render:
1. Builds Docker image (~3 minutes)
2. Creates MySQL database (~3 minutes)
3. Starts services

**You'll see:**
- wordpress-demo: Deploying... → Live
- wordpress-db-demo: Provisioning... → Live

---

## STEP 13: Get MySQL Connection Details
**Time: 2 minutes**

Once mysql service shows "Live":

[ ] Click on: "wordpress-db-demo" service
[ ] Go to: "Info" tab
[ ] Copy these values:
    - **Hostname:** (looks like: mysql-xxxxx.onrender.com)
    - **Database:** wordpress
    - **Username:** (shown in "Connections" section)
    - **Password:** (shown in "Connections" section)

**Save in a text file for next step!**

Example:
```
WORDPRESS_DB_HOST=mysql-abc123.onrender.com
WORDPRESS_DB_NAME=wordpress
WORDPRESS_DB_USER=wordpress_user
WORDPRESS_DB_PASSWORD=strong_random_password
```

---

## STEP 14: Configure Environment Variables
**Time: 2 minutes**

[ ] Click on: "wordpress-demo" service (NOT the database)
[ ] Go to: "Settings" tab
[ ] Scroll down to: "Environment"
[ ] Click: "Add Environment Variable" for each:

Variable 1:
- Key: WORDPRESS_DB_HOST
- Value: (paste from Step 13)
- Click Add

Variable 2:
- Key: WORDPRESS_DB_USER
- Value: (paste from Step 13)
- Click Add

Variable 3:
- Key: WORDPRESS_DB_PASSWORD
- Value: (paste from Step 13)
- Click Add

[ ] All three variables added
[ ] Click: "Save"

Service will automatically restart with new variables (~30 seconds).

---

## STEP 15: Complete WordPress Installation
**Time: 3 minutes**

Once wordpress-demo service shows "Live":

[ ] Go to: "Deployments" tab
[ ] Click on the active deployment
[ ] Scroll right to see: "Render URL"
[ ] Click the URL (looks like: https://wordpress-demo-xxxxx.onrender.com)

WordPress installation wizard will appear:

[ ] Fill in:
    - Site Title: "My Demo Blog"
    - Username: "admin"
    - Password: (choose strong password)
    - Email: your-email@example.com

[ ] Uncheck "Search engine visibility" (optional)
[ ] Click: "Install WordPress"

**Wait 5-10 seconds...**

Success page appears:

[ ] Click: "Log In"
[ ] Login with username "admin" and password from above
[ ] WordPress dashboard appears ✅

---

# PHASE 3: SETUP AUTO-DEPLOYMENT (5 minutes)

## STEP 16: Get Deploy Hook URL
**Time: 1 minute**

[ ] Go to: Render Dashboard → Services → wordpress-demo
[ ] Go to: "Settings" tab
[ ] Scroll down to: "Deploy Hook"
[ ] Copy the URL (entire thing)

Example:
```
https://api.render.com/deploy/srv-abc123?key=xyz789
```

[ ] Save this URL somewhere safe

---

## STEP 17: Add GitHub Secret
**Time: 2 minutes**

[ ] Go to: GitHub repository: https://github.com/YOUR-USERNAME/wordpress-render-demo
[ ] Go to: Settings → Secrets and variables → Actions
[ ] Click: "New repository secret"

[ ] Fill in:
    - Name: RENDER_DEPLOY_HOOK_URL
    - Secret: (paste URL from Step 16)

[ ] Click: "Add secret"

✅ Auto-deploy is now configured!

---

## STEP 18: Test Auto-Deployment
**Time: 3 minutes**

Make a test change:

```bash
# Go to project directory
cd wordpress-render-demo

# Make a small change
echo "# Last updated: $(date)" >> README.md

# Commit and push
git add README.md
git commit -m "Test auto-deployment"
git push origin main
```

[ ] Check GitHub → "Actions" tab
[ ] You should see new workflow running
[ ] Should see: "✅ All checks passed"

Wait 2-3 minutes...

[ ] Go to Render Dashboard → wordpress-demo
[ ] Go to: "Events" tab
[ ] You should see new deployment started
[ ] Wait for "Live" status

[ ] Success! Auto-deployment works! ✅

---

# ✅ CONGRATULATIONS! 

You now have:
✅ WordPress running on Render
✅ MySQL database configured
✅ GitHub integration working
✅ Auto-deployment setup
✅ Production-ready boilerplate

---

# 🧪 FINAL TESTING

## Test 1: Create a Blog Post
[ ] In WordPress admin, go to: Posts → Add New
[ ] Title: "Hello Render!"
[ ] Content: "This post is from my WordPress on Render!"
[ ] Click: "Publish"
[ ] Go to: "View Post"
[ ] Post appears on website ✅

## Test 2: Upload an Image
[ ] Go to: Media → Add New
[ ] Upload an image
[ ] Image appears in media library ✅

## Test 3: Verify Data Persists
[ ] Stop and restart service:
  - Render Dashboard → wordpress-demo → "Settings" → "Restart"
[ ] Wait for restart (30 seconds)
[ ] Visit WordPress again
[ ] Blog post still there ✅
[ ] Image still there ✅

---

# 🎉 YOU'RE DONE!

Your WordPress site is now:
- Hosted on Render
- Version controlled on GitHub
- Auto-deploying on code changes
- Backed by MySQL database
- Ready for custom themes and plugins

---

# 📝 NEXT STEPS

1. **Add Custom Theme**
   - Create theme in: wp-content/themes/my-theme/
   - Push to GitHub → auto-deploys!

2. **Add Custom Plugin**
   - Create plugin in: wp-content/plugins/my-plugin/
   - Push to GitHub → auto-deploys!

3. **Custom Domain**
   - Render Dashboard → Settings → Custom Domains
   - Add your domain
   - Update WordPress Settings

4. **Backups**
   - Install Jetpack plugin in WordPress
   - Enable automatic backups

5. **Monitoring**
   - Monitor WordPress health
   - Check Render logs regularly
   - Setup uptime monitoring

---

# 🆘 TROUBLESHOOTING

### "Database Connection Failed"
**Solution:**
1. Verify WORDPRESS_DB_HOST, USER, PASSWORD are correct
2. Wait 10 minutes - MySQL takes time to initialize
3. Go to Render → wordpress-db-demo → Logs
4. Look for MySQL error messages
5. Reset all variables and try again

### "WordPress Stuck on Installation"
**Solution:**
1. Go to Render → wordpress-demo → Logs
2. Look for error messages
3. Try: Manual deploy button
4. Refresh browser page
5. Clear browser cache (Ctrl+Shift+Delete)

### "Auto-Deploy Not Working"
**Solution:**
1. Check RENDER_DEPLOY_HOOK_URL is set in GitHub Secrets
2. Go to GitHub → Actions tab
3. Check workflow logs for errors
4. Verify deploy.yml file is in .github/workflows/
5. Try manual deploy first from Render

### "Service Keeps Crashing"
**Solution:**
1. Check Render logs for error messages
2. Verify MySQL database is running
3. Check disk space (Render → Services → wordpress-demo → Logs)
4. Try rebuilding with "Manual Deploy"
5. Contact Render support if persists

---

# 💡 TIPS

1. **Always Test Locally First**
   - Use docker-compose.yml for local testing
   - Test themes/plugins locally before pushing

2. **Use Meaningful Commit Messages**
   - "Fix blog layout" is better than "Update"
   - Easier to track changes

3. **Monitor Render Logs**
   - Check logs regularly
   - Catches problems early

4. **Backup Your Database**
   - Install Jetpack backup plugin
   - Export WordPress database monthly

5. **Test Deployments**
   - Make test commits
   - Verify auto-deploy works regularly

---

End of Step-by-Step Guide ✅
"""

with open('STEP_BY_STEP_GUIDE.txt', 'w') as f:
    f.write(step_by_step_guide)

print("✅ Created STEP_BY_STEP_GUIDE.txt")
print("\nGuide includes:")
print("- Phase 1: Local Setup (10 steps)")
print("- Phase 2: Render Deployment (5 steps)")
print("- Phase 3: Auto-Deployment (3 steps)")
print("- Final Testing (3 tests)")
print("- Troubleshooting section")
print("\nTotal: 21 steps with exact instructions")
