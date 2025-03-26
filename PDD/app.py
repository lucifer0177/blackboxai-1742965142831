from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, session
import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime
from model import model
from utils import save_uploaded_file, get_file_path, cleanup_old_files

# Initialize Flask app
app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle image upload and analysis."""
    if request.method == 'POST':
        try:
            # Check if a file was uploaded
            if 'file' not in request.files:
                flash('No file uploaded')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)

            # Save and process the file
            filename = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
            if filename:
                return redirect(url_for('results', filename=filename))
            else:
                flash('Error saving file. Please try again.')
                return redirect(request.url)

        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            flash('An error occurred. Please try again.')
            return redirect(request.url)

    # GET request - show upload form
    return render_template('upload.html')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle AJAX image upload and analysis."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save and process the file
        filename = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        if not filename:
            return jsonify({'error': 'Error saving file. Please try again.'}), 400

        # Get the full path of the saved file
        file_path = get_file_path(filename, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_path):
            return jsonify({'error': 'Error accessing uploaded file. Please try again.'}), 400
        
        # Analyze the image
        diagnosis = model.predict_disease(file_path)
        if not diagnosis:
            return jsonify({'error': 'Error analyzing image. Please try again.'}), 400
        
        # Get care recommendations
        recommendations = model.get_care_recommendations(diagnosis)
        
        # Store results in session
        session['analysis_result'] = {
            'diagnosis': diagnosis,
            'recommendations': recommendations,
            'image_path': filename
        }
        
        return jsonify({
            'success': True,
            'filename': filename,
            'redirect': url_for('results', filename=filename)
        })

    except Exception as e:
        logger.error(f"API upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def results(filename):
    """Display analysis results."""
    try:
        # Get analysis results from session
        analysis_result = session.get('analysis_result', {})
        if not analysis_result:
            # If no results in session, try to analyze again
            file_path = get_file_path(filename, app.config['UPLOAD_FOLDER'])
            if os.path.exists(file_path):
                diagnosis = model.predict_disease(file_path)
                recommendations = model.get_care_recommendations(diagnosis)
                analysis_result = {
                    'diagnosis': diagnosis,
                    'recommendations': recommendations,
                    'image_path': filename
                }
                session['analysis_result'] = analysis_result
            else:
                flash('Image not found. Please upload again.')
                return redirect(url_for('upload'))

        return render_template('results.html', 
                            filename=filename,
                            diagnosis=analysis_result.get('diagnosis'),
                            recommendations=analysis_result.get('recommendations'),
                            image_url=url_for('uploaded_file', filename=filename))
    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}")
        flash('Error displaying results. Please try again.')
        return redirect(url_for('upload'))

@app.route('/forum')
def forum():
    """Render the community forum page."""
    return render_template('forum.html')

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/sw.js')
def service_worker():
    return send_from_directory(os.path.join(app.root_path, 'static', 'js'),
                             'sw.js', mimetype='application/javascript')

@app.route('/offline')
def offline():
    """Render the offline page."""
    return render_template('offline.html')

# Cleanup old files periodically
@app.before_request
def cleanup_uploads():
    """Clean up old uploaded files before processing each request."""
    cleanup_old_files(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Start the Plant Disease Detection server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=args.port)
