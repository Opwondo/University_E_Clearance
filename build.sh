#!/usr/bin/env bash
set -o errexit

# Upgrade pip and install setuptools first
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --no-input

echo "✅ Build completed successfully"
