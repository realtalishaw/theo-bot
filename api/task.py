# api/tasks.py

from utils.api_call import api_call
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def get_all_tasks():
    tasks = api_call("tasks", method='GET')
    if tasks:
        for task in tasks:
            task_id = task.get('id')
            if task_id:
                set_in_cache(f"task:{task_id}", task)

def create_task(task_data):
    response = api_call("tasks", method='POST', data=task_data)
    if response:
        task_id = response.get('id')
        cache_key = f"task:{task_id}"
        set_in_cache(cache_key, response)
    return response

def get_task(task_id):
    cache_key = f"task:{task_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    task_data = api_call(f"tasks/{task_id}", method='GET')
    if task_data:
        set_in_cache(cache_key, task_data)
    return task_data

def update_task(task_id, task_data):
    cache_key = f"task:{task_id}"
    response = api_call(f"tasks/{task_id}", method='PUT', data=task_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_task(task_id):
    cache_key = f"task:{task_id}"
    response = api_call(f"tasks/{task_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response

def get_tasks_by_project(project_id):
    tasks = api_call(f"tasks/byProject/{project_id}", method='GET')
    if tasks:
        for task in tasks:
            task_id = task.get('id')
            if task_id:
                set_in_cache(f"task:{task_id}", task)
    return tasks
