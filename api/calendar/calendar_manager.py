# api/events.py

from utils.api_call import api_call
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def get_all_events():
    events = api_call("events", method='GET')
    if events:
        for event in events:
            event_id = event.get('id')
            if event_id:
                set_in_cache(f"event:{event_id}", event)
    return events

def create_event(event_data):
    response = api_call("events", method='POST', data=event_data)
    if response:
        event_id = response.get('id')
        cache_key = f"event:{event_id}"
        set_in_cache(cache_key, response)
    return response

def get_event(event_id):
    cache_key = f"event:{event_id}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    event_data = api_call(f"events/{event_id}", method='GET')
    if event_data:
        set_in_cache(cache_key, event_data)
    return event_data

def update_event(event_id, event_data):
    cache_key = f"event:{event_id}"
    response = api_call(f"events/{event_id}", method='PUT', data=event_data)
    if response:
        set_in_cache(cache_key, response)
    return response

def delete_event(event_id):
    cache_key = f"event:{event_id}"
    response = api_call(f"events/{event_id}", method='DELETE')
    if response:
        delete_from_cache(cache_key)
    return response

def format_event_as_html(event):
    html = f"<div class='event-card'>"
    html += f"<h2>{event.get('title', 'No Title')}</h2>"
    html += f"<p>{event.get('description', '')}</p>"
    html += f"<p>Date: {event.get('date', 'N/A')}</p>"
    html += "</div>"
    return html

def format_events_as_html(events):
    html = "<div class='events-container'>"
    for event in events:
        html += format_event_as_html(event)
    html += "</div>"
    return html
