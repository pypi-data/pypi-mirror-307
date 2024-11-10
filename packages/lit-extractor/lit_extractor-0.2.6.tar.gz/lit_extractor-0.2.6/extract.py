import click
from helper.helper import *
import requests
from packaging import version

PACKAGE_NAME='lit-extractor'
CURRENT_VERSION='0.2.6'

def check_for_update():
    try:
        # Get the latest version from PyPI
        response = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json")
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]

        # Compare the current version with the latest version
        if version.parse(latest_version) > version.parse(CURRENT_VERSION):
            console.print(f"\nA new version [green]{latest_version}[/] is available! You have [red]{CURRENT_VERSION}[/].")
            console.print("Run the following command to update:\n")
            console.print(f"\n  pip install --upgrade {PACKAGE_NAME}\n", style="green bold underline")
        console.rule()
    except requests.RequestException as e:
        console.print_exception(f"Error checking for update: {e}", err=True)


@click.group()
def extract():
    check_for_update()


@extract.command()
@click.argument('file', type=click.File('r'))
@click.option("-o","--output", default='extracted_list',show_default=True, help="Output file name where the extracted list is to be stored")
@click.option("-d", "--download", is_flag=True,default=False,show_default=True, help="flag to download all the books in the url")
def url(file, output, download):
    original_url_list = extract_urls_from_file(file)
    extracted_url = []
    for item in original_url_list:
        result = fff_url_extractor(item)
        processed_result = prettify_url(result)
        extracted_url.extend(processed_result)

    filename = save_to_file(output, extracted_url)
    console.print(f"All the urls in the file [cyan]{file.name}[/] has been processed", style="bold green")
    console.rule()
    if download:
        download_url_from_file(filename)

    val = rich_prompt("\nDo you want to open the file? (y/N) ")
    if val == 'y' or val == 'Y':
        open_in_editor(filename)


@extract.command()
@click.argument('file', type=click.Path())
def download(file):
    download_url_from_file(file)


if __name__ == '__main__':
    url()
