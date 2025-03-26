import os

# Flask configuration
SECRET_KEY = os.urandom(32)
DEBUG = True

# File upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Session configuration
SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
