#!/usr/bin/env bash
set -o errexit

# Show Python version for debugging
python --version

# Upgrade pip and install essential build tools
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --no-input

echo "✅ Build completed successfully on Python $(python --version)"
