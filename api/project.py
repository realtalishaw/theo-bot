# api/projects.py

from utils.api_call import api_call
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def get_all_projects():
    projects = api_call("projects", method='GET')
    if projects:
        for project in projects:
            project_id = project.get('id')
            if project_id:
                set_in_cache(f"project:{project_id}", project)

def create_project(project_data):
    response = api_call("projects", method='POST', data=project_data)
    if response:
        project_id = response.get('id')
        cache_key = f"project:{project_id}"
        set_in_cache(cache_key, response)
    return response

def get_project(project_id):
    cache_key = f"project:{project_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    project_data = api_call(f"projects/{project_id}", method='GET')
    if project_data:
        set_in_cache(cache_key, project_data)
    return project_data

def update_project(project_id, project_data):
    cache_key = f"project:{project_id}"
    response = api_call(f"projects/{project_id}", method='PUT', data=project_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_project(project_id):
    cache_key = f"project:{project_id}"
    response = api_call(f"projects/{project_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response

def get_projects_by_moon(moon_id):
    projects = api_call(f"projects/byMoon/{moon_id}", method='GET')
    if projects:
        # Optionally, cache these projects too
        for project in projects:
            project_id = project.get('id')
            if project_id:
                set_in_cache(f"project:{project_id}", project)
    return projects
