from click import style
import click
import platform
from tqdm import tqdm
import fanficfare
import os
import sys
import time
import subprocess
from rich.console import Console
from rich.traceback import install
install()

console = Console()


def extract_urls_from_file(filename):
    data_from_file = filename.readlines()
    data_from_file = [url.strip() for url in data_from_file]
    return data_from_file


def fff_url_extractor(url):
    try:
        console.print(f"Processing {url}", style="yellow")
        result = subprocess.run(['fanficfare', '-l', url], capture_output=True, text=True, check=True)
        metadata = result.stdout
        return metadata
    except subprocess.CalledProcessError as e:
        console.print(f"Error downloading [bold]{url}[/]: {e}", style="red")
        return ""


def download_url_from_file(file):
    try:
        console.print(f"Downloading from {file}", style="yellow")
        result = subprocess.Popen(['fanficfare', '-o', "is_adult=true", '-i', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with tqdm(total=100, desc="Downloading", ncols=100) as progress_bar:
            while result.poll() is None:  # While subprocess is running
                print(result.stdout, end='')
                time.sleep(0.5)  # Small delay to slow down the loop
                progress_bar.update(1)  # Simulate progress with small increments
                if progress_bar.n >= progress_bar.total:
                    progress_bar.n = 0  # Reset bar if it reaches max (optional)
                    progress_bar.refresh()
                    progress_bar.update(1)
        # Update bar to full on completion
            progress_bar.n = 100
            progress_bar.refresh()

    # Get the subprocess output
        stdout, stderr = result.communicate()
        if result.returncode == 0:
            console.print("Download completed successfully.", style="green")
        else:
            console.print("Download failed.", style="red")
            console.print(stderr.decode("utf-8"), style="red")
    except subprocess.CalledProcessError as e:
        console.print(f"Error downloading from [bold]{file}[/]: {e}", style="red")
        return ""


def prettify_url(url):
    url_list = url.strip().split('\n')
    return url_list


def save_to_file(file_name=None, file_data=None):
    name = f"{file_name}.txt" if file_name else "extracted_list.txt"
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, name)
    try:
        with open(file_path, 'w') as f:
            if file_data is not None:
                for line in file_data:
                    f.write(f"{line}\n")
            console.print(f"Data has been saved to [cyan]{file_path}[/]", style="green")
    except IOError as e:
        console.print(f"Error writing to [bold]{file_path}[/]: {e}", style="red")
        return

    return file_path

def open_in_editor(filename):
    # Prompt for filename if not provided
    if not filename:
        filename = click.prompt("Please enter the filename to open", type=str)

    # Check if the file exists, create it if not
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("")  # Create an empty file
        click.echo(f"Created a new file: {filename}")

    # Open the file with the default editor based on OS
    try:
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filename])
        else:  # Linux and other UNIX-based systems
            subprocess.run(["xdg-open", filename])
    except Exception as e:
        click.echo(f"Error opening file: {e}")

def rich_prompt(prompt_text, style="bold cyan"):
    console.print(f"[{style}]{prompt_text}[/{style}]", end=" ")
    return input()  # Capture input after the styled prompt
