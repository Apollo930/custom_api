from api import app  # Import your Flask app from api.py
import vercel_wsgi

# Export the app for Vercel
app = vercel_wsgi.app
