# Web Archive Downloader

A simple Python application that downloads a website's content using the Wayback Machine and saves its HTML and associated resources (such as images, scripts, and CSS files) locally.

## Features

- **Download Website**: Enter a URL, and the application will download its archived version from the Wayback Machine.
- **Save HTML**: The main HTML page of the website is saved locally as `index.html`.
- **Save Resources**: All referenced resources like images, scripts, and stylesheets are downloaded and stored in a `resources` folder.

## Requirements

- Python 3.x
- Required libraries:
  - `tkinter` (for GUI)
  - `requests` (for making HTTP requests)
  - `beautifulsoup4` (for parsing HTML and extracting resource links)

To install the necessary libraries, run the following:

```bash
pip install requests beautifulsoup4
```

## How to Use

1. Clone or download this repository to your local machine.
2. Ensure you have Python 3.x and the required libraries installed.
3. Run the script using the following command:

```bash
python web_archive_downloader.py
```
