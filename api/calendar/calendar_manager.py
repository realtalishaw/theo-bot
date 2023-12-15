import requests
import json
from typing import Dict, Any

# Base URL for the calendar API
# You should replace this with the actual URL of your API
API_BASE_URL = "https://your-api-endpoint.com/calendar"

# Headers to be used in the API request
# Replace 'your-access-token' with the actual token if authentication is needed
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-access-token"
}

def create_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new calendar event.
    
    :param event_data: A dictionary containing the details of the event.
    :return: The response from the API.
    """
    response = requests.post(f"{API_BASE_URL}/events", headers=HEADERS, data=json.dumps(event_data))
    return response.json()

def get_event(event_id: str) -> Dict[str, Any]:
    """
    Retrieves a specific calendar event by ID.
    
    :param event_id: The unique identifier of the event.
    :return: The response from the API.
    """
    response = requests.get(f"{API_BASE_URL}/events/{event_id}", headers=HEADERS)
    return response.json()

def update_event(event_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates a specific calendar event by ID.
    
    :param event_id: The unique identifier of the event.
    :param update_data: A dictionary containing the updated details of the event.
    :return: The response from the API.
    """
    response = requests.put(f"{API_BASE_URL}/events/{event_id}", headers=HEADERS, data=json.dumps(update_data))
    return response.json()

def delete_event(event_id: str) -> Dict[str, Any]:
    """
    Deletes a specific calendar event by ID.
    
    :param event_id: The unique identifier of the event to delete.
    :return: The response from the API.
    """
    response = requests.delete(f"{API_BASE_URL}/events/{event_id}", headers=HEADERS)
    return response.json()

def list_events() -> Dict[str, Any]:
    """
    Lists all the calendar events.
    
    :return: The response from the API.
    """
    response = requests.get(f"{API_BASE_URL}/events", headers=HEADERS)
    return response.json()

def format_calendar_event_as_html(event_info: Dict[str, Any]) -> str:
    """
    Formats a calendar event's information as HTML for presentation.
    
    :param event_info: A dictionary containing the details of the event.
    :return: A string of HTML representing the event.
    """
    # This is a simple HTML representation.
    # You may want to create a more complex HTML based on your needs.
    event_html = f"<div><h1>{event_info['title']}</h1><p>{event_info['description']}</p></div>"
    return event_html
