This Python package reproduces the Tesseract/OCR path used in MORT.

## Requirements

The package is intended to run on a WSL system. It creates a Windows Tesseract
process to perform OCR function.

## Usage

### Clone and install

```
git clone https://github.com/spectrumbranch/mortar.git
cd mortar/python-project
python -m venv .venv
. .venv/bin/activate

pip install .[dev]
```

### Set the required environment variables

The package requires these variables be set. Actual values vary between
configurations.

Path to the Tesseract executable:

```
export TESSERACT="$VCPKG_INSTALLED/x64-windows-static-md/x64-windows-static-md/tools/tesseract/tesseract.exe"
```

Path to the `tessdata` directory installed with MORT:

```
export TESSERACT_DATA="C:/MORT/MORT/bin/x64/Release/net7.0-windows10.0.22621.0/tessdata"
```

### Run the tests

```
nox
```

### Use the command line interface

Paths must be absolute paths on a WSL filesystem (i.e. begin with `/mnt`).

```
mortess /mnt/c/path/to/some/mort_capture.png
```
