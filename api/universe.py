import requests

# Base URL for the Universe API
UNIVERSE_API_URL = "https://your-api-endpoint.com/universe"

def create_universe_entity(entity_data):
    """
    Creates a new universe entity (planet, moon, or satellite).
    
    :param entity_data: Information about the entity to create.
    :return: The response from the API.
    """
    # Implement API call to create a new universe entity

def get_universe_entity(entity_id):
    """
    Retrieves details of a universe entity.
    
    :param entity_id: ID of the entity to retrieve.
    :return: The formatted HTML details of the entity.
    """
    # Implement API call to get details of a universe entity
    # ...

def update_universe_entity(entity_id, entity_data):
    """
    Updates an existing universe entity.
    
    :param entity_id: ID of the entity to update.
    :param entity_data: New data for updating the entity.
    :return: The response from the API.
    """
    # Implement API call to update a universe entity
    # ...

def delete_universe_entity(entity_id):
    """
    Deletes a universe entity.
    
    :param entity_id: ID of the entity to delete.
    :return: The response from the API.
    """
    # Implement API call to delete a universe entity
    # ...

def format_universe_response_as_html(response_data):
    """
    Formats a universe entity's information as HTML for presentation.
    
    :param response_data: The API response data containing entity details.
    :return: A string of HTML representing the entity.
    """
    # This is where you would convert the response data into a user-friendly HTML format.
    # For example:
    html_representation = f"<div>"
    for key, value in response_data.items():
        html_representation += f"<p><strong>{key.capitalize()}:</strong> {value}</p>"
    html_representation += "</div>"
    
    return html_representation
