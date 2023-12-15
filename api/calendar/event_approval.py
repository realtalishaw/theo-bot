import requests
from calendar_manager import create_event

# Assuming you have a separate API endpoint for event approval requests
APPROVAL_API_URL = "https://your-api-endpoint.com/approval"

def request_event_approval(event_data, user_info):
    """
    Sends an event approval request to an admin.

    :param event_data: A dictionary containing the details of the event.
    :param user_info: Information about the user who is requesting the event.
    :return: The response from the approval API.
    """
    # The payload might include the event data along with the user's information
    payload = {
        "event": event_data,
        "user": user_info
    }
    
    # Send the event approval request to the admin
    response = requests.post(APPROVAL_API_URL, json=payload)
    # Here you might want to include error handling and check the response status
    
    return response.json()

def approve_event(event_id, admin_decision):
    """
    Processes the admin's decision to approve or reject an event.

    :param event_id: The unique identifier of the event to be approved.
    :param admin_decision: The decision from the admin, either 'approve' or 'reject'.
    :return: A message indicating the outcome.
    """
    # If approved, create the event using the previously defined function
    if admin_decision == 'approve':
        # Retrieve the event details from a temporary storage where it was saved during the approval request
        # For now, let's assume it's just passed directly for simplicity
        event_details = retrieve_event_details(event_id)
        
        # Create the event using the calendar_manager function
        create_event_response = create_event(event_details)
        
        # Return the success response or handle it as needed
        return create_event_response
    else:
        # Handle rejection case
        return {"message": "Event creation request has been rejected."}

def retrieve_event_details(event_id):
    """
    Placeholder function to retrieve event details.
    This should interface with the storage where you keep events pending approval.
    
    :param event_id: The unique identifier of the event.
    :return: The event details.
    """
    # Implement the retrieval of event details from temporary storage
    # For now, return a mock event details dictionary
    return {
        "title": "Mock Event",
        "description": "This is a mock event for approval process",
        # ... include other necessary event details
    }
