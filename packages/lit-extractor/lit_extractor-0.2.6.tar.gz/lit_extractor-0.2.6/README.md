# Literotica URL Extractor CLI Tool

This tool allows users to extract and download URLs from fanfiction sites using `FanFicFare`. It supports processing URLs from a file, saving extracted URLs to a new file, and downloading all stories from those URLs. The tool is designed for fanfiction enthusiasts and researchers who want a streamlined way to manage and download content from various fanfiction sources.

## Features

- **Extract URLs**: Reads a file with URLs, processes each to list available stories on that page, and saves all URLs to a specified output file.
- **Download Stories**: Allows downloading stories listed in a file with extracted URLs.
- **Progress Tracking**: Uses `tqdm` to display download progress.

## Requirements

- Python 3.6 or later
- [Click](https://pypi.org/project/click/) - For creating the CLI
- [tqdm](https://pypi.org/project/tqdm/) - For progress bars
- [FanFicFare](https://pypi.org/project/FanFicFare/) - The core library for extracting and downloading fanfiction
- [Pygments](https://pypi.org/project/Pygments/) - Syntax highlighting (optional)

To install dependencies, run:
```bash
pip install -r requirements.txt
Installation
Clone the repository and navigate to the folder:

bash
Copy code
git clone https://github.com/username/literotica-url-extractor.git
cd literotica-url-extractor
Install the tool:

bash
Copy code
pip install .
Usage
The tool provides two primary commands: url and download.

1. Extract URLs from File (url)
Extracts all URLs from a text file, processes them using FanFicFare, and saves the extracted list to a specified output file. This command can also download the stories from the URLs if the --d flag is used.

Usage:

bash
Copy code
literotica url <path_to_file> [OPTIONS]
Arguments:

<path_to_file>: Path to the text file containing a list of URLs.
Options:

--o: Output file name to save the extracted URLs. If omitted, defaults to extracted_list.txt.
--d: If set to True, downloads all the stories from the extracted URLs.
Example:

bash
Copy code
literotica url urls.txt --o extracted_urls.txt --d True
In this example:

urls.txt is the input file containing URLs to be processed.
The extracted URLs are saved in extracted_urls.txt.
The --d True option initiates the download of all listed stories.
2. Download Stories from File (download)
Downloads all stories listed in the provided file.

Usage:

bash
Copy code
literotica download <file>
Arguments:

<file>: Path to the file containing URLs of the stories to download.
Example:

bash
Copy code
literotica download extracted_urls.txt
In this example:

extracted_urls.txt is the file containing URLs to download.
Example Workflow
Extract URLs and Save to a File

bash
Copy code
literotica url urls.txt --o extracted_urls.txt
This command extracts URLs from urls.txt and saves them in extracted_urls.txt.

Download Stories from Extracted URLs

bash
Copy code
literotica download extracted_urls.txt
Downloads all stories from the URLs listed in extracted_urls.txt.

Code Structure
extract_urls_from_file: Reads and cleans URL list from a file.
fff_url_extractor: Calls FanFicFare to list all stories for a given URL.
download_url_from_file: Initiates story download from URLs in a file with progress tracking using tqdm.
prettify_url: Formats URLs for better readability.
save_to_file: Saves processed URLs to a file, appending to an existing file or creating a new one.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request.