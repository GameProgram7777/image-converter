#!/bin/bash
# Script to configure GitHub repository metadata using the GitHub CLI (gh)

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed. Please install it first: https://cli.github.com/"
else
    echo "Setting repository description..."
    gh repo edit --description "A powerful, universal desktop application for converting between 50+ image and metadata formats (including RAW, HDR, and Web formats)."

    echo "Setting repository topic tags..."
    gh repo edit --add-topic "python,tkinter,imagemagick,image-converter,batch-processing,exif,heic,raw-converter"

    echo "Repository metadata configured successfully!"
fi

echo "Note: To enable GitHub Pages, navigate to your Repository Settings > Pages on GitHub.com and select the 'docs/' folder on your main branch."
