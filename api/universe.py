# api/universe.py

from utils.api_call import api_call
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

# Satellite Functions
def create_satellite(satellite_data):
    response = api_call("satellites", method='POST', data=satellite_data)
    return response

def get_satellite(satellite_id):
    cache_key = f"satellite:{satellite_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    satellite_data = api_call(f"satellites/{satellite_id}", method='GET')
    if satellite_data:
        set_in_cache(cache_key, satellite_data)
    return satellite_data

def update_satellite(satellite_id, satellite_data):
    cache_key = f"satellite:{satellite_id}"
    response = api_call(f"satellites/{satellite_id}", method='PUT', data=satellite_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_satellite(satellite_id):
    cache_key = f"satellite:{satellite_id}"
    response = api_call(f"satellites/{satellite_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response

# Moon Functions
def get_all_moons():
    moons = api_call("moons", method='GET')
    return moons

def get_moon(moon_id):
    cache_key = f"moon:{moon_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    moon_data = api_call(f"moons/{moon_id}", method='GET')
    if moon_data:
        set_in_cache(cache_key, moon_data)
    return moon_data

def update_moon(moon_id, moon_data):
    cache_key = f"moon:{moon_id}"
    response = api_call(f"moons/{moon_id}", method='PUT', data=moon_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_moon(moon_id):
    cache_key = f"moon:{moon_id}"
    response = api_call(f"moons/{moon_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response

def get_moons_by_planet(planet_id):
    moons = api_call(f"moons/byPlanet/{planet_id}", method='GET')
    return moons

# Planet Functions
def get_all_planets():
    planets = api_call("planets", method='GET')
    return planets

def create_planet(planet_data):
    response = api_call("planets", method='POST', data=planet_data)
    return response

def get_planet(planet_id):
    cache_key = f"planet:{planet_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    planet_data = api_call(f"planets/{planet_id}", method='GET')
    if planet_data:
        set_in_cache(cache_key, planet_data)
    return planet_data

def update_planet(planet_id, planet_data):
    cache_key = f"planet:{planet_id}"
    response = api_call(f"planets/{planet_id}", method='PUT', data=planet_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_planet(planet_id):
    cache_key = f"planet:{planet_id}"
    response = api_call(f"planets/{planet_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response
