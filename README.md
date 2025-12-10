# scan-image

A command-line tool to scan a folder of images and detect whether they contain a specific text phrase using OCR (Tesseract). Supports multiprocessing, perceptual hashing for duplicate suppression and useful logging.

---

### Features
- OCR phrase search via Tesseract  
- Duplicate removal using perceptual hashing  
- Parallel processing for fast scanning  
- Supports all common image formats (JPG, JPEG, PNG, BMP, TIFF)

---

### Installation

## Installation

1. **Clone the repository**

```powershell
git clone https://github.com/wbc1wan/scan-image.git
cd scan-image
```

2. **Create and activate a virtual environment**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. **Upgrade pip, setuptools, and wheel**

```powershell
python -m pip install --upgrade pip setuptools wheel
```

4. **Install the package in editable mode**

```powershell
pip install -e .
```

---

## Tesseract Setup

1. Install Tesseract OCR from [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract).  

2. Set the path in your environment (PowerShell):

```powershell
$env:TESSERACT_PATH="C:\Program Files\Tesseract-OCR\tesseract.exe"
```

3. Verify Tesseract is accessible:

```powershell
& $env:TESSERACT_PATH --version
```

> Note: You do not need to add Tesseract to your PATH if you set `TESSERACT_PATH`.

---

## Usage

### Command Line

```powershell
scan-image --folder "C:\path\to\images" --phrase "YOUR_PHRASE"
```

- If folder or phrase is omitted, the CLI will ask interactively.
- Duplicates are removed automatically.
- Results are logged to the console.

---

## Testing

Tests are in the `tests` folder and include unit and integration tests.

### Run all tests with coverage:

```powershell
coverage run --source=scan_image -m unittest discover -s tests -v
coverage report -m
coverage html
```

### Run a single test file:

```powershell
coverage run --source=scan_image -m unittest discover -s tests -p "test_real_image.py" -v
```

---

### Project Structure

```
scan-image/
├── .coverage
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── tree.txt
├── .github/
│   └── workflows/
│       └── image_scanner_ci.yml
├── scan_image/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── scanner.py
│   └── utils.py
├── scan_image.egg-info/
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── PKG-INFO
│   ├── requires.txt
│   ├── SOURCES.txt
│   └── top_level.txt
└── tests/
    ├── test_config.py
    ├── test_logger.py
    ├── test_real_image.py
    ├── test_scanner.py
    └── test_utils.py
```

---

### License

MIT License © wbc1wan(WanAnis)
