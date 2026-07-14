# Universal Image Converter

**Description:**
A powerful, universal desktop application for converting between 50+ image and metadata formats (including RAW, HDR, Web, and GIS formats). Built with Python and Tkinter, and powered by ImageMagick to provide the broadest possible format support while maintaining a highly responsive UI during batch operations.

## Features
- **Massive Format Support:** Converts standard formats (JPG, PNG), Camera RAW, Apple HEIC, HDR, Medical imaging, and EXIF profiles.
- **Batch Processing:** Seamlessly convert hundreds of images at once.
- **Dynamic JSON Database:** Extension capabilities are driven entirely by a configurable `format_database.json`.
- **Responsive UI:** Built with Python/Tkinter, featuring background threading.

## Installation
You need Python 3 and ImageMagick installed on your system.

**Ubuntu/Debian:**
```bash
sudo apt-get update && sudo apt-get install imagemagick
```

**macOS:**
```bash
brew install imagemagick
```

## Usage
```bash
python image_converter.py
```
