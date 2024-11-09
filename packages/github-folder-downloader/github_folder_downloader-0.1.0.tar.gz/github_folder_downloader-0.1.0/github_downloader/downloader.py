import requests
import os
import re
from typing import Tuple

def download_file(url: str, dest_folder: str) -> None:
    """Download a single file from GitHub and save it to the destination folder."""
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.join(dest_folder, url.split('/')[-1])
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

def download_content(repo: str, path: str, branch: str, dest_folder: str) -> None:
    """
    Recursively download content from a specified GitHub repository path.
    Handles both files and folders within the path.
    """
    api_url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        content = response.json()
        if isinstance(content, dict):  # Single file
            download_file(content['download_url'], dest_folder)
        else:  # Directory
            for item in content:
                if item['type'] == 'file':
                    download_file(item['download_url'], dest_folder)
                elif item['type'] == 'dir':
                    download_content(repo, item['path'], branch, os.path.join(dest_folder, item['name']))
    else:
        print(f"Failed to retrieve contents at: {api_url}")

def parse_github_url(url: str) -> Tuple[str, str, str]:
    """Extract the repository name, branch, and path from a GitHub URL."""
    match = re.match(r"https://github\.com/([^/]+)/([^/]+)/(tree|blob)/([^/]+)(?:/(.+))?", url)
    if match:
        repo = f"{match.group(1)}/{match.group(2)}"
        branch = match.group(4)
        path = match.group(5) if match.group(5) else ""
        return repo, branch, path
    else:
        raise ValueError("Invalid GitHub URL format. Please ensure it follows the pattern: https://github.com/username/repo/(tree|blob)/branch[/path]")

def download_from_github(url: str, dest_folder: str = "./downloaded_files") -> None:
    """
    Main function to download content from GitHub.
    
    Args:
        url (str): GitHub URL to download from
        dest_folder (str): Destination folder for downloads
    """
    try:
        repo, branch, path = parse_github_url(url)
        print(f"Downloading content from {repo}/{path} on branch {branch}...")
        download_content(repo, path, branch, dest_folder)
    except ValueError as e:
        print(e) 