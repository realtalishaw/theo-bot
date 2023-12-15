import requests
from typing import List, Dict, Any

# Base URL for the files API, which is backed by AWS Lambda & S3
FILES_API_URL = "https://your-api-endpoint.com/files"

# Headers for API authentication/authorization
# Replace 'your-access-token' with the actual token if needed
HEADERS = {
    "Authorization": "Bearer your-access-token"
}

# Roles permitted to update/delete files
PERMITTED_ROLES = ['SUPER_ADMIN', 'ADMIN', 'PROJECT_LEAD']

def check_permission(user_role):
    """
    Check if the user has permission to update or delete the file.
    
    :param user_role: Role of the user performing the operation.
    :return: True if permitted, False otherwise.
    """
    return user_role in PERMITTED_ROLES

def create_file(file_data, user_info):
    """
    Creates a new file entry and uploads it to AWS S3.
    
    :param file_data: Information about the file such as planet, moons, etc.
    :param user_info: Information about the user uploading the file.
    :return: The response from the API.
    """
    # Include user_info to track who uploaded the file
    payload = {**file_data, "uploaded_by": user_info['username']}
    response = requests.post(FILES_API_URL, headers=HEADERS, json=payload)
    return response.json()

def get_file(file_name):
    """
    Retrieves a single file from AWS S3.
    
    :param file_name: Name of the file to retrieve.
    :return: The direct link to the file or content to download.
    """
    response = requests.get(f"{FILES_API_URL}/{file_name}", headers=HEADERS)
    file_link = response.json().get('file_link')
    
    # Code to download the file and return its content goes here
    # For Telegram, you will likely use the bot API to send the file directly to the user
    
    return file_link

def get_files_list(file_criteria: Dict[str, Any]):
    """
    Retrieves a list of files based on certain criteria.
    
    :param file_criteria: Dictionary with search criteria like planet, moons, etc.
    :return: A list of file names that match the criteria.
    """
    response = requests.get(FILES_API_URL, headers=HEADERS, json=file_criteria)
    files_list = response.json().get('files')
    return files_list

def update_file(file_name, file_data, user_role):
    """
    Updates a file's metadata or content in AWS S3.
    
    :param file_name: Name of the file to update.
    :param file_data: New data to update the file with.
    :param user_role: Role of the user performing the operation.
    :return: The response from the API.
    """
    if not check_permission(user_role):
        return {"error": "You do not have permission to update files."}
    
    response = requests.put(f"{FILES_API_URL}/{file_name}", headers=HEADERS, json=file_data)
    return response.json()

def delete_file(file_name, user_role):
    """
    Deletes a file from AWS S3.
    
    :param file_name: Name of the file to delete.
    :param user_role: Role of the user performing the operation.
    :return: The response from the API.
    """
    if not check_permission(user_role):
        return {"error": "You do not have permission to delete files."}
    
    response = requests.delete(f"{FILES_API_URL}/{file_name}", headers=HEADERS)
    return response.json()
