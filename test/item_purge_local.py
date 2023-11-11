import boto3
from botocore.exceptions import ClientError
import json

dynamodb = boto3.client('dynamodb')
table_name = 'DTABLE_NAME_TO_BE_CHANGED'
deleted_table_name = 'Records_Deleted'

def lambda_handler(event, context):
    print(event, context)
    # Backup the table
    try:
        backup_response = dynamodb.create_backup(
            TableName=table_name,
            BackupName=f"{table_name}-backup-{context.get('aws_request_id')}"
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error backing up the DynamoDB table: {e}")
        }

    # Extract the DB_ID from the event
    db_id = event['DB_ID']
    if not db_id:
        return {
            'statusCode': 400,
            'body': json.dumps("No DB_ID provided in input")
        }

    # Check if the item exists
    try:
        get_response = dynamodb.get_item(
            TableName=table_name,
            Key={'DB_ID': {'S': db_id}}
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error fetching the item from DynamoDB table: {e}")
        }

    # If the item does not exist, return a message
    if 'Item' not in get_response:
        print(f'db id not exist : {db_id}')
        return {
            'statusCode': 404,
            'body': json.dumps("The record doesn't exist")
        }

    # Backup the item to be deleted
    item = get_response['Item']
    try:
        dynamodb.put_item(
            TableName=deleted_table_name,
            Item=item
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error backing up the item to {deleted_table_name}: {e}")
        }

    # If the item exists, proceed to delete it
    try:
        delete_response = dynamodb.delete_item(
            TableName=table_name,
            Key={'DB_ID': {'S': db_id}}
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting the item from DynamoDB table: {e}")
        }

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps(f"Item with DB_ID {db_id} deleted successfully")
    }
