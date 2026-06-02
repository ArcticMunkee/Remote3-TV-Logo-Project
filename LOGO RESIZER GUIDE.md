# LOGO RESIZER GUIDE

This guide explains how to use the `logo_resizer.py` script.

The script converts image files from a folder into PNG files. Every converted image is placed on a transparent `500x500 px` canvas with proportional resizing and `10 px` padding.

You do not need programming knowledge to use this guide.

[logo_resizer.py](https://github.com/ArcticMunkee/Remote3-TV-Logo-Project/blob/main/logo_resizer.py)

## What This Script Does

The script can be started with a source folder directly from the command line, or it can ask you for a folder interactively.

It then scans this folder and all subfolders for supported image files.

Supported file types are:

```text
.png
.jpg
.jpeg
.webp
.bmp
.gif
.tif
.tiff
```

Every supported image is converted into a PNG file.

The result is always:

```text
500x500 px
PNG format
transparent background
10 px padding
proportional resizing
```

The original files are not changed.

By default, the converted files are written to a `converted_png_500` subfolder inside your selected source folder.

## What You Need

Before using the script, you need three things:

```text
1. Python installed on your computer
2. The Pillow image library installed
3. The logo_resizer.py file from this repository
```

## Step 1: Download the Script

Open this repository on GitHub.

Download the file:

```text
logo_resizer.py
```

Save it somewhere easy to find, for example:

```text
Downloads
```

or create a dedicated folder such as:

```text
Logo-Converter
```

## Step 2: Install Python

The script requires Python 3.

### macOS

Open the Terminal app.

Check if Python is already installed:

```bash
python3 --version
```

If you see a version number, for example:

```text
Python 3.12.0
```

Python is installed.

If Python is not installed, download it from:

```text
https://www.python.org/downloads/
```

Install Python and then run the command again:

```bash
python3 --version
```

### Windows

Open Command Prompt or PowerShell.

Check if Python is already installed:

```powershell
python --version
```

If you see a version number, Python is installed.

If Python is not installed, download it from:

```text
https://www.python.org/downloads/
```

During installation, make sure to enable:

```text
Add python.exe to PATH
```

Then close and reopen Command Prompt or PowerShell and check again:

```powershell
python --version
```

## Step 3: Install Pillow

Pillow is the image library used by the script.

### macOS

Open Terminal and run:

```bash
python3 -m pip install pillow
```

### Windows

Open Command Prompt or PowerShell and run:

```powershell
python -m pip install pillow
```

If the installation worked, you should see a message that Pillow was installed successfully.

## Step 4: Prepare Your Image Folder

Put all images you want to convert into one folder.

Example:

```text
My Logos
```

The folder can also contain subfolders.

The script will process images inside the selected folder and inside its subfolders.

Example:

```text
My Logos
├── channel-logos
├── misc
└── test-icons
```

## Step 5: Start the Script With a Source Folder

Open Terminal, Command Prompt, or PowerShell.

Navigate to the folder where `logo_resizer.py` is saved.

### macOS Example

If the script is in this folder:

```bash
~/Downloads/logo-resizer
```

and your images are in this folder:

```bash
~/Downloads/images-to-resize
```

run:

```bash
cd ~/Downloads/logo-resizer
python3 logo_resizer.py ~/Downloads/images-to-resize
```

The converted files will be written to:

```text
~/Downloads/images-to-resize/converted_png_500
```

### Windows Example

If the script is in this folder:

```powershell
$env:USERPROFILE\Downloads\logo-resizer
```

and your images are in this folder:

```powershell
$env:USERPROFILE\Downloads\images-to-resize
```

run:

```powershell
cd $env:USERPROFILE\Downloads\logo-resizer
python logo_resizer.py $env:USERPROFILE\Downloads\images-to-resize
```

The converted files will be written to:

```text
%USERPROFILE%\Downloads\images-to-resize\converted_png_500
```

In this direct command mode, files with `mosaic` in the name are skipped by default and smaller logos are not upscaled by default.

## Optional: Choose a Different Output Folder

If you do not want the default `converted_png_500` subfolder, use `--output-dir`.

### macOS Example

```bash
python3 logo_resizer.py ~/Downloads/images-to-resize --output-dir ~/Downloads/resized_logos
```

### Windows Example

```powershell
python logo_resizer.py $env:USERPROFILE\Downloads\images-to-resize --output-dir $env:USERPROFILE\Downloads\resized_logos
```

If a custom output folder already exists, the script writes into it and overwrites files with the same names. It does not delete the whole custom output folder unless you add `--clean-output`.

## Optional: Include Mosaic Files or Upscale Small Logos

Use `--include-mosaics` if files with `mosaic` in the filename should also be processed:

```bash
python3 logo_resizer.py ~/Downloads/images-to-resize --include-mosaics
```

Use `--upscale` if smaller logos should be enlarged to use more of the 500x500 px canvas:

```bash
python3 logo_resizer.py ~/Downloads/images-to-resize --upscale
```

Both options can be combined:

```bash
python3 logo_resizer.py ~/Downloads/images-to-resize --include-mosaics --upscale
```

## Alternative: Start Interactive Mode

You can also start the script without a source folder:

### macOS

```bash
python3 logo_resizer.py
```

### Windows

```powershell
python logo_resizer.py
```

## Step 6: Enter the Source Folder in Interactive Mode

After starting the script, it asks:

```text
Enter source folder:
```

Enter the full path to the folder that contains your images.

### macOS Example

```text
/Users/yourname/Downloads/My Logos
```

### Windows Example

```text
C:\Users\yourname\Downloads\My Logos
```

Instead of typing the folder path manually, you can also drag the folder directly into the Terminal, Command Prompt, or PowerShell window.

This automatically inserts the correct folder path for you.

After the folder path appears, press Enter.

## Step 7: Choose Whether Mosaic Files Should Be Included

The script asks:

```text
Should files with 'mosaic' in the name also be processed? (y/N):
```

Recommended answer:

```text
n
```

or simply press Enter.

Why?

Files with `mosaic` in the name are often overview images or combined preview sheets. Usually, these should not be converted as individual logos.

Use:

```text
y
```

only if you are sure you want to include them.

## Step 8: Choose Whether Small Logos Should Be Upscaled

The script asks:

```text
Should smaller logos be upscaled? (y/N):
```

Recommended answer:

```text
n
```

or simply press Enter.

Why?

If a small logo is enlarged, it may look blurry.

Use:

```text
y
```

only if you want small logos to be enlarged to use more of the `500x500 px` canvas.

## Step 9: Wait Until the Script Is Finished

The script now converts the images.

For every processed file, you will see a line like this:

```text
OK: example.jpg -> example.png
```

If a file cannot be processed, you may see:

```text
ERROR:
```

The script continues with the next file.

## Step 10: Find the Converted PNG Files

By default, the script creates a new output folder inside your original source folder.

If your source folder is called:

```text
My Logos
```

the output folder will be called:

```text
converted_png_500
```

Example:

```text
My Logos
├── channel-logos
├── misc
├── test-icons
└── converted_png_500
```

The converted PNG files are inside the new folder.

Your original files remain unchanged.

## Output Format

Every successfully converted file has these properties:

```text
File format: PNG
Image size: 500x500 px
Background: transparent
Padding: 10 px
Scaling: proportional
```

This means logos keep their original proportions. They are not stretched or distorted.

## Important Notes

The script deletes the old output folder before creating a new one.

For example, if this folder already exists:

```text
converted_png_500
```

the script deletes it and creates it again.

This prevents old files from being mixed with newly converted files.

Only the output folder is deleted.

The original source folder is not deleted or changed.

This automatic deletion only applies to the default `converted_png_500` output folder. If you use a custom `--output-dir`, the script does not delete that folder unless you also add `--clean-output`.

## Common Problems

### Problem: `No module named PIL`

This means Pillow is not installed.

Install it with:

### macOS

```bash
python3 -m pip install pillow
```

### Windows

```powershell
python -m pip install pillow
```

### Problem: `python: command not found`

Python is not installed or not correctly available in the command line.

Install Python from:

```text
https://www.python.org/downloads/
```

On Windows, make sure to enable:

```text
Add python.exe to PATH
```

### Problem: The folder path is not accepted

Make sure the folder path really exists.

If the path contains spaces, this is usually fine when the script asks for the folder path directly.

Example:

```text
/Users/yourname/Downloads/My Logos
```

### Problem: Some files were skipped

Files are skipped if they are not supported image files.

Supported formats are:

```text
.png
.jpg
.jpeg
.webp
.bmp
.gif
.tif
.tiff
```

Files with `mosaic` in the name are skipped unless you choose to include them.

## Recommended Basic Usage

For most users, the best workflow is:

```text
1. Put all images into one folder.
2. Run logo_resizer.py with that folder path.
3. Use the PNG files from the converted_png_500 subfolder.
```

Example:

```bash
python3 logo_resizer.py ~/Downloads/images-to-resize
```

## What the Script Is Useful For

This script is useful when you need logo files that all have the same technical format.

For example:

```text
TV channel logos
remote control icons
media center artwork
Home Assistant icons
Unfolded Circle Remote 3 icons
```

The script helps make different logo files consistent without manually editing every image.
