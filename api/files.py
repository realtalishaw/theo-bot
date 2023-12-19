# api/files.py

from utils.api_call import api_call
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def get_all_files():
    files = api_call("files", method='GET')
    if files:
        for file in files:
            file_id = file.get('id')
            if file_id:
                set_in_cache(f"file:{file_id}", file)

def create_file(file_data):
    response = api_call("files", method='POST', data=file_data)
    if response:
        file_id = response.get('id')
        cache_key = f"file:{file_id}"
        set_in_cache(cache_key, response)
    return response

def get_file(file_id):
    cache_key = f"file:{file_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    file_data = api_call(f"files/{file_id}", method='GET')
    if file_data:
        set_in_cache(cache_key, file_data)
    return file_data

def update_file(file_id, file_data):
    cache_key = f"file:{file_id}"
    response = api_call(f"files/{file_id}", method='PUT', data=file_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_file(file_id):
    cache_key = f"file:{file_id}"
    response = api_call(f"files/{file_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response

def get_files_by_moon(moon_id):
    files = api_call(f"files/moon/{moon_id}", method='GET')
    if files:
        for file in files:
            file_id = file.get('id')
            if file_id:
                set_in_cache(f"file:{file_id}", file)
    return files

def get_files_by_task(task_id):
    files = api_call(f"files/task/{task_id}", method='GET')
    if files:
        for file in files:
            file_id = file.get('id')
            if file_id:
                set_in_cache(f"file:{file_id}", file)
    return files

def get_files_by_project(project_id):
    files = api_call(f"files/project/{project_id}", method='GET')
    if files:
        for file in files:
            file_id = file.get('id')
            if file_id:
                set_in_cache(f"file:{file_id}", file)
    return files
