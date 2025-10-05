from flask import Flask
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import your Flask app
from app import app

# Export for Vercel
app = app