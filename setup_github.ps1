# NYC Taxi Project - GitHub Setup Script (PowerShell)
# 
# This script initializes the Git repository and sets up the project for GitHub

Write-Host "🚀 Setting up NYC Taxi Project for GitHub..." -ForegroundColor Green

# Check if Git is installed
try {
    git --version | Out-Null
    Write-Host "✅ Git is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Initialize Git repository if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "📦 Git repository already exists" -ForegroundColor Blue
}

# Set up Git configuration
Write-Host "⚙️ Checking Git configuration..." -ForegroundColor Yellow

$currentUser = git config user.name
$currentEmail = git config user.email

if (-not $currentUser) {
    $username = Read-Host "Please enter your Git username"
    git config user.name $username
}

if (-not $currentEmail) {
    $email = Read-Host "Please enter your Git email"
    git config user.email $email
}

$configuredUser = git config user.name
$configuredEmail = git config user.email
Write-Host "✅ Git user: $configuredUser <$configuredEmail>" -ForegroundColor Green

# Add all files to staging
Write-Host "📝 Adding files to Git staging..." -ForegroundColor Yellow
git add .

# Check status
Write-Host "📊 Current Git status:" -ForegroundColor Blue
git status

# Create initial commit
$defaultMessage = "Initial commit: NYC Taxi Analytics Pipeline"
$commitMessage = Read-Host "Enter commit message (press Enter for default: '$defaultMessage')"
if (-not $commitMessage) {
    $commitMessage = $defaultMessage
}

Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m $commitMessage

Write-Host ""
Write-Host "🎉 Git repository setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps to push to GitHub:" -ForegroundColor Cyan
Write-Host "1. Create a new repository on GitHub" -ForegroundColor White
Write-Host "2. Run: git remote add origin https://github.com/YOUR_USERNAME/NYC_Taxi_Project.git" -ForegroundColor White
Write-Host "3. Run: git branch -M main" -ForegroundColor White
Write-Host "4. Run: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "📁 Repository structure ready for GitHub with:" -ForegroundColor Cyan
Write-Host "   ✅ Comprehensive .gitignore" -ForegroundColor Green
Write-Host "   ✅ Directory structure with .gitkeep files" -ForegroundColor Green
Write-Host "   ✅ Detailed README.md" -ForegroundColor Green
Write-Host "   ✅ Requirements.txt with version pinning" -ForegroundColor Green
Write-Host "   ✅ Well-commented source code" -ForegroundColor Green
Write-Host "   ✅ MIT License" -ForegroundColor Green

Write-Host ""
Write-Host "🔗 Quick GitHub repository creation:" -ForegroundColor Magenta
Write-Host "Visit: https://github.com/new" -ForegroundColor White
