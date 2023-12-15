import requests

# Base URL for the JIRA API
JIRA_API_URL = "https://your-jira-instance.atlassian.net/rest/api/3"

# Roles permitted to create, update, or delete projects
PERMITTED_ROLES = ['PROJECT_ROLE_SPECIFIC_TO_PROJECT', 'SUPER_ADMIN', 'ADMIN', 'PROJECT_LEAD']

def check_project_permission(user_role, project_id=None):
    """
    Check if the user has permission to C, U, D on the specific project.
    
    :param user_role: Role of the user performing the operation.
    :param project_id: ID of the project for specific role checks.
    :return: True if permitted, False otherwise.
    """
    # If it's a super admin, admin, or project lead, always return True
    if user_role in PERMITTED_ROLES[:3]:
        return True
    
    # Here you would implement a check to see if the user has the specific role
    # for the given project_id. This will likely involve a call to your backend
    # to get the user's roles for that project.
    
    return False

def create_project(project_data, user_role):
    """
    Creates a new project in JIRA.
    
    :param project_data: Information about the project to create.
    :param user_role: Role of the user attempting to create the project.
    :return: The response from JIRA.
    """
    if not check_project_permission(user_role):
        return {"error": "You do not have permission to create projects."}
    
    # Add code to send a POST request to JIRA API to create a project
    # ...

def get_project(project_id):
    """
    Retrieves a project from JIRA.
    
    :param project_id: ID of the project to retrieve.
    :return: The project details.
    """
    # Add code to send a GET request to JIRA API to retrieve a project
    # ...

def update_project(project_id, project_data, user_role):
    """
    Updates a project's details in JIRA.
    
    :param project_id: ID of the project to update.
    :param project_data: New data for updating the project.
    :param user_role: Role of the user attempting to update the project.
    :return: The response from JIRA.
    """
    if not check_project_permission(user_role, project_id):
        return {"error": "You do not have permission to update this project."}
    
    # Add code to send a PUT request to JIRA API to update a project
    # ...

def delete_project(project_id, user_role):
    """
    Deletes a project from JIRA.
    
    :param project_id: ID of the project to delete.
    :param user_role: Role of the user attempting to delete the project.
    :return: The response from JIRA.
    """
    if not check_project_permission(user_role, project_id):
        return {"error": "You do not have permission to delete this project."}
    
    # Add code to send a DELETE request to JIRA API to delete a project
    # ...
