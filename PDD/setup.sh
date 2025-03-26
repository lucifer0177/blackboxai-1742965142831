#!/bin/bash

# Create directory structure
mkdir -p templates static/css static/js static/images uploads

# Download Python files
echo "Downloading Python files..."
files=("app.py" "config.py" "model.py" "utils.py" "requirements.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" .
    fi
done

# Download template files
echo "Downloading template files..."
template_files=("404.html" "500.html" "base.html" "forum.html" "index.html" "offline.html" "results.html" "upload.html")
for file in "${template_files[@]}"; do
    if [ -f "templates/$file" ]; then
        cp "templates/$file" templates/
    fi
done

# Download static files
echo "Downloading static files..."
if [ -f "static/css/style.css" ]; then
    cp "static/css/style.css" static/css/
fi

if [ -f "static/js/app.js" ]; then
    cp "static/js/app.js" static/js/
fi

if [ -f "static/js/sw.js" ]; then
    cp "static/js/sw.js" static/js/
fi

if [ -f "static/images/favicon.ico" ]; then
    cp "static/images/favicon.ico" static/images/
fi

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! Run 'python app.py' to start the application."
