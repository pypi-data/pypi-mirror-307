import logging
from botocore.exceptions import ClientError
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Constants for DynamoDB primary and secondary keys
DYNAMODB_PRIMARY_KEY = "GSI1PK"
DYNAMODB_SECONDARY_KEY = "GSI1SK"

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def check_resource_exists(table_name, org_id, resource_id):
    """
    Checks if a resource with the given resource_id exists for the specified org_id in the specified DynamoDB table.
    
    Parameters:
    - table_name: Name of the DynamoDB table to query.
    - org_id: The organization ID for the resource.
    - resource_id: The ID of the resource to check.
    
    Returns:
    - True if the resource exists, False otherwise.
    """
    # Verify that resource id is an integer
    if not isinstance(resource_id, int):
        return False

    # Initialize the table using the table name
    table = dynamodb.Table(table_name)
    key_to_query = {
        DYNAMODB_PRIMARY_KEY: f"{org_id}_resource",
        DYNAMODB_SECONDARY_KEY: resource_id
    }

    try:
        logger.info(f"Checking if resource exists in table '{table_name}' with key: {key_to_query}")
        response = table.get_item(Key=key_to_query)
        return 'Item' in response  # Returns True if the resource exists, False otherwise

    except ClientError as e:
        logger.error(f"DynamoDB client error while checking resource: {e}")
        raise e
