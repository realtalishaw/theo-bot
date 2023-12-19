# api/user.py

from utils.api_call import api_call
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def get_user(user_id):
    cache_key = f"user:{user_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    user_data = api_call(f"users/{user_id}", method='GET')
    if user_data:
        set_in_cache(cache_key, user_data)
    return user_data

def create_user(user_data):
    print("we're inside of create user")
    response = api_call("users", method='POST', data=user_data)
    if response:
        user_id = response.get('id')
        cache_key = f"user:{user_id}"
        set_in_cache(cache_key, response)
    return response

def update_user(user_id, user_data):
    cache_key = f"user:{user_id}"
    response = api_call(f"users/{user_id}", method='PUT', data=user_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_user(user_id):
    cache_key = f"user:{user_id}"
    response = api_call(f"users/{user_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response

def get_all_users():
    users = api_call("users", method='GET')
    if users:
        for user in users:
            user_id = user.get('id')
            if user_id:
                set_in_cache(f"user:{user_id}", user)
