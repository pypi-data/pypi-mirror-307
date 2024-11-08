import os
import shutil
import requests

def read_file(file_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path to the directory of this file
    data_path = os.path.join(root_dir, '..', 'data', file_name)
    
    with open(data_path, 'r') as file:
        content = file.read()
    
    return content

def export_file(file_name, destination_dir='.'):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path to the directory of this file
    data_path = os.path.join(root_dir, '..', 'data', file_name)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"{file_name} not found in the data directory.")

    # Get the absolute path of the destination directory (defaults to current directory)
    destination_path = os.path.abspath(destination_dir)

    # Copy the file to the destination directory
    shutil.copy(data_path, os.path.join(destination_path, file_name))
    
    return f"File {file_name} exported successfully to {destination_path}."

def all_files():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    
    # List all files in the data directory
    try:
        files = os.listdir(data_dir)
        file_list = [file for file in files if os.path.isfile(os.path.join(data_dir, file))]
        
        # Print the list of files
        print("Files in data directory:")
        for file in file_list:
            print(file)
    
    except FileNotFoundError:
        print(f"Data directory {data_dir} not found.")
        
def remote_read(file_name):
    # Replace these with your GitHub repo details
    owner = "feedbackwebx"  # e.g., "octocat"
    repo = "cloud"    # e.g., "Hello-World"
    
    # URL to access the raw content of the file
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{file_name}"

    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    elif response.status_code == 404:
        return f"File '{file_name}' not found in the repository."
    else:
        return f"Error retrieving file: {response.status_code} - {response.reason}"

def remote_export(file_name, owner="feedbackwebx", repo="cloud"):
    # URL to access the raw content of the file in the GitHub repo
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{file_name}"

    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the file to the current directory
        with open(os.path.basename(file_name), 'w') as local_file:
            local_file.write(response.text)
        return f"File '{file_name}' exported successfully to the current directory."
    elif response.status_code == 404:
        return f"File '{file_name}' not found in the repository."
    else:
        return f"Error retrieving file: {response.status_code} - {response.reason}"