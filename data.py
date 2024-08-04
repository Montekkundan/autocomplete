import time
from datetime import datetime
import os
import requests
from github import Github
from colorama import init, Fore, Style
import re

init(autoreset=True)

end_time = time.time()
start_time = end_time - 86400

with open("token.txt", "r") as token_file:
    ACCESS_TOKEN = token_file.read().strip()

g = Github(ACCESS_TOKEN)
authenticated_user = g.get_user()
print(f"Authenticated User: {authenticated_user.login}")

headers = {
    'Authorization': f'token {ACCESS_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Checkpoint file for saving the state
CHECKPOINT_FILE = "checkpoint.txt"


def sanitize_filename(filename):
    """
    Sanitize filenames by replacing invalid characters.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def load_checkpoint():
    """Load the last processed index from the checkpoint file."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as cp_file:
            return int(cp_file.read().strip())
    return 0


def save_checkpoint(index_to_save):
    """Save the current index to the checkpoint file."""
    with open(CHECKPOINT_FILE, "w") as cp_file:
        cp_file.write(str(index_to_save))


def download_py_files(contents, download_dir):
    """
    Recursively download .py files from the GitHub repository contents.

    Args:
        contents (list): List of file/directory contents from the GitHub API.
        download_dir (str): The local directory path to save files.
    Returns:
        bool: True if any .py files were downloaded, False otherwise.
    """
    py_files_downloaded = False

    for content_item in contents:
        # If the item is a file and has a .py extension, download it
        if content_item['type'] == 'file' and content_item['name'].endswith('.py'):
            download_url = content_item['download_url']
            # Sanitize the file path
            safe_path = sanitize_filename(content_item['path'])
            file_path = os.path.join(download_dir, safe_path)

            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                file_response = requests.get(download_url)
                with open(file_path, 'wb') as py_file:
                    py_file.write(file_response.content)
                print(Fore.CYAN + Style.BRIGHT + f"Downloaded: {file_path}")

                py_files_downloaded = True
            except OSError as e:
                print(Fore.RED + Style.BRIGHT + f"Failed to download {file_path}: {str(e)}")
                continue

        # If the item is a directory, recursively traverse it
        elif content_item['type'] == 'dir':
            dir_url = f"https://api.github.com/repos/{repository.full_name}/contents/{content_item['path']}"
            dir_response = requests.get(dir_url, headers=headers)
            dir_contents = dir_response.json()

            # Recursive call
            if download_py_files(dir_contents, download_dir):
                py_files_downloaded = True

    return py_files_downloaded


start_index = load_checkpoint()

for interval in range(3):
    try:
        start_time_str = datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d')
        end_time_str = datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d')
        query = f"language:python created:{start_time_str}..{end_time_str}"

        print(query)
        result = g.search_repositories(query)
        total_repositories = result.totalCount
        print(total_repositories)

        for repo_idx, repository in enumerate(result, start=1):
            if repo_idx <= start_index:
                continue  # Skip already processed repositories

            print(
                Fore.CYAN + Style.BRIGHT +
                f"Processing repository {repo_idx}/{total_repositories}: {repository.full_name}"
            )

            # Get the contents of the repository's root directory
            repo_url = f"https://api.github.com/repos/{repository.full_name}/contents"
            response = requests.get(repo_url, headers=headers)
            repo_contents = response.json()

            # Attempt to download .py files
            repository_dir = f"repos/{repository.owner.login}/{repository.name}"
            if not download_py_files(repo_contents, repository_dir):
                print(
                    Fore.YELLOW + Style.BRIGHT +
                    f"Skipped repository: {repository.full_name} (No .py files found)"
                )

            print(Fore.CYAN + Style.BRIGHT + f"Current start time: {start_time_str}")

            # Save progress
            save_checkpoint(repo_idx)

        end_time -= 86400
        start_time -= 86400
    except Exception as e:
        print(str(e))
        print(Fore.RED + Style.BRIGHT + "Broke for some reason...")
        time.sleep(200)

print("Finished, your new end time is: ", end_time)
