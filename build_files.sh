#!/bin/bash

# Install Node.js dependencies
npm install

# Build Tailwind CSS with v4 CLI
npm run build-css-prod

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear