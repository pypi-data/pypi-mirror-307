# audit.py

import json
import boto3
import logging
import time
from botocore.exceptions import ClientError
import decimal

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize the SQS client
sqs_client = boto3.client('sqs')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return float(o)
        return super(DecimalEncoder, self).default(o)

def create_audit_record(org_id, audit_queue_url, uid, action, endpoint, source, payload):
    """
    Sends an audit record to an SQS queue.
    
    Args:
        org_id (str): Organization ID for the audit record.
        audit_queue_url (str): The URL of the SQS queue to send the record to.
        uid (str): User ID of the action initiator.
        action (str): Action performed (e.g., "create").
        endpoint (str): Endpoint accessed (e.g., "/resource/createResource").
        source (str): Source of the action (e.g., "appApi").
        payload (dict): The data payload of the audit record.
    
    Returns:
        dict: A response dictionary with status code and message.
    """
    try:
        # Create the message to send to SQS
        message_body = {
            "org_id": org_id,
            "timestamp": int(round(time.time() * 1000)),  # Current time in milliseconds
            "source": source,
            "endpoint": endpoint,
            "action": action,
            "uid": uid,
            "payload": payload
        }

        # Send the message to the SQS queue
        response = sqs_client.send_message(
            QueueUrl=audit_queue_url,
            MessageBody=json.dumps(message_body, cls=DecimalEncoder)
        )
        logger.info(f"SQS response: {response}")
        return {'statusCode': 200,
                'body': json.dumps({'message': 'Audit record sent to SQS successfully'})}
    except ClientError as e:
        logger.error(f"SQS client error: {e}")
        return {'statusCode': 500,
                'body': json.dumps({'message': 'SQS client error'})}
