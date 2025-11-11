
# Create the validation script file that can be run
validation_script = '''#!/bin/bash

echo "=========================================="
echo "WordPress-Render-GitHub Demo Validator"
echo "=========================================="
echo ""

# Color codes
GREEN='\\033[0;32m'
RED='\\033[0;31m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

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
if grep -q "FROM wordpress" Dockerfile 2>/dev/null; then
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

if grep -q "services:" render.yaml 2>/dev/null && grep -q "wordpress-demo" render.yaml 2>/dev/null; then
  echo -e "${GREEN}✅${NC} render.yaml contains web service"
else
  echo -e "${RED}❌${NC} render.yaml missing web service configuration"
  ERRORS=$((ERRORS + 1))
fi

if grep -q "pserv" render.yaml 2>/dev/null || grep -q "mysql" render.yaml 2>/dev/null; then
  echo -e "${GREEN}✅${NC} render.yaml contains database service"
else
  echo -e "${RED}❌${NC} render.yaml missing database service"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 4: Validate GitHub workflow
echo "🔄 Validating GitHub workflow..."
if [ -f ".github/workflows/deploy.yml" ]; then
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
else
  echo -e "${RED}❌${NC} GitHub workflow file missing"
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
    echo -e "${YELLOW}⚠️${NC} Git remote 'origin' not configured yet (you'll set this up next)"
  fi
else
  echo -e "${YELLOW}⚠️${NC} Not in a Git repository (clone from GitHub first)"
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
  echo "Fix the errors above and run this script again"
  exit 1
fi
'''

with open('validate-setup.sh', 'w') as f:
    f.write(validation_script)

print("✅ Created validate-setup.sh")
print("\nTo use:")
print("1. chmod +x validate-setup.sh")
print("2. ./validate-setup.sh")
