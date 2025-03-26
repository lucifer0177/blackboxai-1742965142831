# AI-Driven Plant Care Assistant

An intelligent web application for plant disease diagnosis and care recommendations.

## Quick Download & Setup

### Option 1: Using Setup Script (Easiest)

1. Download these files:
   - `setup.sh`
   - `requirements.txt`

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. Create folders:
```bash
mkdir -p templates static/css static/js static/images uploads
```

2. Download all files into their respective folders:
- Main folder: `app.py`, `config.py`, `model.py`, `utils.py`, `requirements.txt`
- `templates/`: All HTML files
- `static/css/`: `style.css`
- `static/js/`: `app.js`, `sw.js`
- `static/images/`: `favicon.ico`

3. Set up Python:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Start Application

1. Activate environment:
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Run server:
```bash
python app.py
```

3. Visit http://localhost:5000

## Need Help?

1. Check file locations match structure below
2. Ensure Python 3.8+ is installed
3. Verify virtual environment is activated
4. Try manual setup if script fails

## File Structure
```
plant-care-assistant/
├── app.py
├── config.py
├── model.py
├── utils.py
├── requirements.txt
├── setup.sh
├── templates/
│   └── (HTML files)
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── uploads/
```

## License

MIT License
