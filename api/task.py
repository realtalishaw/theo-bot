import requests

# Base URL for the JIRA API for tasks
JIRA_API_TASK_URL = "https://your-jira-instance.atlassian.net/rest/api/3/issue"

# Roles permitted to create, update, or delete tasks
TASK_PERMITTED_ROLES = ['PROJECT_ROLE_SPECIFIC_TO_PROJECT', 'SUPER_ADMIN', 'ADMIN', 'PROJECT_LEAD']

def check_task_permission(user_role, project_id=None):
    """
    Check if the user has permission to C, U, D tasks within the specific project.
    
    :param user_role: Role of the user performing the operation.
    :param project_id: ID of the project for specific role checks.
    :return: True if permitted, False otherwise.
    """
    # Implement role check logic, similar to the project permission check

def create_task(task_data, user_role):
    """
    Creates a new task in JIRA.
    
    :param task_data: Information about the task to create.
    :param user_role: Role of the user attempting to create the task.
    :return: The response from JIRA.
    """
    if not check_task_permission(user_role):
        return {"error": "You do not have permission to create tasks."}
    
    # Implement the API call to create a task in JIRA

def get_task(task_id):
    """
    Retrieves a task from JIRA.
    
    :param task_id: ID of the task to retrieve.
    :return: The task details.
    """
    # Implement the API call to get a task from JIRA

def update_task(task_id, task_data, user_role):
    """
    Updates a task's details in JIRA.
    
    :param task_id: ID of the task to update.
    :param task_data: New data for updating the task.
    :param user_role: Role of the user attempting to update the task.
    :return: The response from JIRA.
    """
    if not check_task_permission(user_role):
        return {"error": "You do not have permission to update this task."}
    
    # Implement the API call to update a task in JIRA

def delete_task(task_id, user_role):
    """
    Deletes a task from JIRA.
    
    :param task_id: ID of the task to delete.
    :param user_role: Role of the user attempting to delete the task.
    :return: The response from JIRA.
    """
    if not check_task_permission(user_role):
        return {"error": "You do not have permission to delete this task."}
    
    # Implement the API call to delete a task in JIRA
