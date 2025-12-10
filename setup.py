from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scan-image",  # Package name
    version="0.1.0",
    author="WanAnis",
    description="Scan a folder of images and detect a specific text phrase using OCR (Tesseract)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pillow",
        "pytesseract",
        "opencv-python",
        "imagehash",
        "numpy",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "scan-image=scan_image.scanner:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
    ],
    include_package_data=True,
)
