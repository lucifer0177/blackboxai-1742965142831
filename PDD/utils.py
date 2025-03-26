import os
import logging
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    if not filename or '.' not in filename:
        logger.warning(f"Invalid filename: {filename}")
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    allowed = ext in ALLOWED_EXTENSIONS
    if not allowed:
        logger.warning(f"Invalid file extension: {ext}")
    return allowed

def get_file_path(filename, upload_folder):
    """Get the full path for a file in the upload folder."""
    return os.path.join(upload_folder, filename)

def save_uploaded_file(file, upload_folder):
    """
    Save the uploaded file securely and return the filename.
    Returns None if file is invalid.
    """
    try:
        if not file:
            logger.error("No file provided")
            return None

        if not allowed_file(file.filename):
            logger.warning(f"Invalid file type: {file.filename}")
            return None

        # Create a unique filename to avoid overwrites
        original_filename = secure_filename(file.filename)
        name, ext = os.path.splitext(original_filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}{ext}"
        
        # Ensure upload directory exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save the file
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Verify file was saved successfully
        if os.path.exists(filepath):
            logger.info(f"File saved successfully: {filename}")
            return filename
        else:
            logger.error(f"File save verification failed: {filename}")
            return None

    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return None

def cleanup_old_files(upload_folder, max_age_hours=24):
    """Clean up files older than max_age_hours."""
    try:
        current_time = time.time()
        for filename in os.listdir(upload_folder):
            filepath = os.path.join(upload_folder, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > (max_age_hours * 3600):
                    try:
                        os.remove(filepath)
                        logger.info(f"Cleaned up old file: {filename}")
                    except Exception as e:
                        logger.error(f"Error removing old file {filename}: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning up files: {str(e)}")
