#!/bin/bash

# Exit on error
set -e

echo "🔨 Starting build process..."

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build Tailwind CSS with v4 CLI
echo "🎨 Building Tailwind CSS..."
npm run build-css-prod

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"