@echo off
REM Script to configure GitHub repository metadata using the GitHub CLI (gh) on Windows

REM Check if gh CLI is installed
where gh >nul 2>nul
if %errorlevel% neq 0 (
    echo GitHub CLI ^(gh^) is not installed. Please install it first: https://cli.github.com/
    pause
    goto :eof
)

echo Setting repository description...
gh repo edit --description "A powerful, universal in-browser web application for converting between 50+ image and metadata formats (including RAW, HDR, and EXIF)."

echo Setting repository topic tags...
gh repo edit --add-topic "python,tkinter,imagemagick,image-converter,batch-processing,exif,heic,raw-converter"

echo Repository metadata configured successfully!
echo Note: To enable GitHub Pages, navigate to your Repository Settings ^> Pages on GitHub.com and select the 'docs/' folder on your main branch.
pause
