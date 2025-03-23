from neon_api import NeonAPI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Neon API client
neon = NeonAPI(api_key=os.environ["NEON_API_KEY"])

# User functions


def get_current_user():
    return neon.me()


# API Key Management
def list_api_keys():
    return neon.api_keys()


def create_api_key(**json):
    return neon.api_key_create(**json)


def delete_api_key(key_id):
    return neon.api_key_delete(key_id)


# Project Management
def list_projects():
    try:
        response = neon.projects()

        return format_action_response(response)

    except Exception as e:
        return f"❌ Error creating project: {str(e)}"


def get_project(project_id):
    return neon.project(project_id)


def create_project(project_name: str):
    """
    Creates a new project and returns a user-friendly message.
    """
    try:
        response = neon.project_create(
            project={
                "name": project_name,
                "pg_version": 17,  # Fixed typo: removed extra colon
                "region_id": "azure-eastus2",
            }
        )

        # Format the response before returning
        return format_action_response(response)

    except Exception as e:
        return f"❌ Error creating project: {str(e)}"


def update_project(project_id: str, **json):
    return neon.project_update(project_id, **json)


def delete_project(project_id: str):
    return neon.project_delete(project_id)


def get_project_permissions(project_id: str):
    return neon.project_permissions(project_id)


def grant_project_permissions(project_id: str, **json):
    return neon.project_permissions_grant(project_id, **json)


def revoke_project_permissions(project_id: str, **json):
    return neon.project_permissions_revoke(project_id, **json)


def get_connection_uri(project_id: str, database_name: str, role_name: str):
    return neon.connection_uri(project_id, database_name, role_name)


# Branch Management
def list_branches(project_id: str):
    return neon.branches(project_id)


def get_branch(project_id: str, branch_id: str):
    return neon.branch(project_id, branch_id)


def create_branch(project_id: str, branch_name: str):
    return neon.branch_create(project_id, json={"branch": {"name": branch_name}})


def update_branch(project_id: str, branch_id: str, **json):
    return neon.branch_update(project_id, branch_id, **json)


def delete_branch(project_id: str, branch_id: str):
    return neon.branch_delete(project_id, branch_id)


def set_primary_branch(project_id: str, branch_id: str):
    return neon.branch_set_as_primary(project_id, branch_id)


# Database Management
def list_databases(project_id: str, branch_id: str):
    return neon.databases(project_id, branch_id)


def get_database(project_id: str, branch_id: str, database_id: str):
    return neon.database(project_id, branch_id, database_id)


def create_database(project_id: str, branch_id: str, database_name: str):
    return neon.database_create(
        project_id, branch_id, json={"database": {"name": database_name}}
    )


def update_database(project_id: str, branch_id: str, **json):
    return neon.database_update(project_id, branch_id, **json)


def delete_database(project_id: str, branch_id: str, database_id: str):
    return neon.database_delete(project_id, branch_id, database_id)


# Endpoint Management
def list_endpoints(project_id: str, branch_id: str):
    return neon.endpoints(project_id, branch_id)


def create_endpoint(project_id: str, branch_id: str, **json):
    return neon.endpoint_create(project_id, branch_id, **json)


def update_endpoint(project_id: str, branch_id: str, endpoint_id: str, **json):
    return neon.endpoint_update(project_id, branch_id, endpoint_id, **json)


def delete_endpoint(project_id: str, branch_id: str, endpoint_id: str):
    return neon.endpoint_delete(project_id, branch_id, endpoint_id)


def start_endpoint(project_id: str, branch_id: str, endpoint_id: str):
    return neon.endpoint_start(project_id, branch_id, endpoint_id)


def suspend_endpoint(project_id: str, branch_id: str, endpoint_id: str):
    return neon.endpoint_suspend(project_id, branch_id, endpoint_id)


# Role Management
def list_roles(project_id: str, branch_id: str):
    return neon.roles(project_id, branch_id)


def get_role(project_id: str, branch_id: str, role_name: str):
    return neon.role(project_id, branch_id, role_name)


def create_role(project_id: str, branch_id: str, role_name: str):
    return neon.role_create(project_id, branch_id, role_name)


def delete_role(project_id: str, branch_id: str, role_name: str):
    return neon.role_delete(project_id, branch_id, role_name)


def reveal_role_password(project_id: str, branch_id: str, role_name: str):
    return neon.role_password_reveal(project_id, branch_id, role_name)


def reset_role_password(project_id: str, branch_id: str, role_name: str):
    return neon.role_password_reset(project_id, branch_id, role_name)


# Operation Management
def list_operations(project_id: str):
    return neon.operations(project_id)


def get_operation(project_id: str, operation_id: str):
    return neon.operation(project_id, operation_id)


# Experimental
def get_consumption():
    return neon.consumption()


def format_action_response(response):
    """
    Formats responses for various actions in a user-friendly way.

    :param response: The response object from the API.
    :return: A formatted string message.
    """
    if hasattr(response, "dict"):  # Convert response object to dictionary if needed
        response = response.dict()

    if isinstance(response, dict):
        if "project" in response:
            project = response["project"]
            return f"✅ Project '{project.get('name', 'Unknown')}' (ID: {project.get('id', 'N/A')}) created successfully in '{project.get('region_id', 'N/A')}' with PostgreSQL v{project.get('pg_version', 'N/A')}."

        if "branch" in response:
            branch = response["branch"]
            return f"✅ Branch '{branch.get('name', 'Unknown')}' (ID: {branch.get('id', 'N/A')}) created successfully."

        if "database" in response:
            database = response["database"]
            return f"✅ Database '{database.get('name', 'Unknown')}' (ID: {database.get('id', 'N/A')}) created successfully."

        if "role" in response:
            role = response["role"]
            return f"✅ Role '{role.get('name', 'Unknown')}' created successfully."

    return "✅ Action is completed successfully."
