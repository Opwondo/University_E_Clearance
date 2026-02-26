"""
Wrapper for Render to find the Django application
"""
from e_clearance.wsgi import application

# This allows both 'app:app' and 'e_clearance.wsgi:application' to work
app = application
