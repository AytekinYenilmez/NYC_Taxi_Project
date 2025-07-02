#!/bin/bash
# NYC Taxi Project - GitHub Setup Script
# 
# This script initializes the Git repository and sets up the project for GitHub

echo "🚀 Setting up NYC Taxi Project for GitHub..."

# Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "📦 Git repository already exists"
fi

# Set up Git configuration (update with your details)
echo "⚙️ Checking Git configuration..."
if [ -z "$(git config user.name)" ]; then
    echo "Please enter your Git username:"
    read username
    git config user.name "$username"
fi

if [ -z "$(git config user.email)" ]; then
    echo "Please enter your Git email:"
    read email
    git config user.email "$email"
fi

echo "✅ Git user: $(git config user.name) <$(git config user.email)>"

# Add all files to staging
echo "📝 Adding files to Git staging..."
git add .

# Check status
echo "📊 Current Git status:"
git status

# Create initial commit
echo "💾 Creating initial commit..."
read -p "Enter commit message (default: 'Initial commit: NYC Taxi Analytics Pipeline'): " commit_msg
commit_msg=${commit_msg:-"Initial commit: NYC Taxi Analytics Pipeline"}
git commit -m "$commit_msg"

echo ""
echo "🎉 Git repository setup complete!"
echo ""
echo "📋 Next steps to push to GitHub:"
echo "1. Create a new repository on GitHub"
echo "2. Run: git remote add origin https://github.com/AytekinYenilmez/NYC_Taxi_Project.git"
echo "3. Run: git branch -M main"
echo "4. Run: git push -u origin main"
echo ""
echo "📁 Repository structure ready for GitHub with:"
echo "   ✅ Comprehensive .gitignore"
echo "   ✅ Directory structure with .gitkeep files"
echo "   ✅ Detailed README.md"
echo "   ✅ Requirements.txt with version pinning"
echo "   ✅ Well-commented source code"
