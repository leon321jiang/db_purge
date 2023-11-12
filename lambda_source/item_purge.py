import boto3
from botocore.exceptions import ClientError
import json

dynamodb = boto3.client('dynamodb')
db_list_table_name = 'onboarded_db_list'
deleted_table_name = 'records_deleted'

def lambda_handler(event, context):
    print(event)
    # Backup the table
    try:
        backup_response = dynamodb.create_backup(
            TableName=db_list_table_name,
            BackupName=f"{db_list_table_name}-backup-{context.aws_request_id}"
        )
        print(f'backup {db_list_table_name} successful for request {context.aws_request_id}')
    except ClientError as e:
        print(f"Error backing up the DynamoDB table: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error backing up the DynamoDB table: {e}")
        }

    # Extract the db_name from the event
    db_name = event['db_name']
    if not db_name:
        print("No db_name provided in input")
        return {
            'statusCode': 400,
            'body': json.dumps("No db_name provided in input")
        }

    # Check if the item exists
    try:
        get_response = dynamodb.get_item(
            TableName=db_list_table_name,
            Key={'db_name': {'S': db_name}}
        )
        print(f'{get_response} successfull get')
    except ClientError as e:
        print(f"Error fetching the item from DynamoDB table: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error fetching the item from DynamoDB table: {e}")
        }

    # If the item does not exist, return a message
    if 'Item' not in get_response:
        print(f'db id not exist : {db_name}')
        return {
            'statusCode': 404,
            'body': json.dumps("The record doesn't exist")
        }

    # Backup the item to be deleted
    item = get_response['Item']
    try:
        print(f"trying to backup db_name {db_name}")
        dynamodb.put_item(
            TableName=deleted_table_name,
            Item=item
        )
    except ClientError as e:
        print(f"Error backing up the item to {deleted_table_name}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error backing up the item to {deleted_table_name}: {e}")
        }
    print(f'succesfully backed up the item {db_name} to {deleted_table_name}')

    # If the item exists, proceed to delete it
    try:
        print(f"trying to delete db_name {db_name}")
        delete_response = dynamodb.delete_item(
            TableName=db_list_table_name,
            Key={'db_name': {'S': db_name}}
        )
    except ClientError as e:
        print(f"Error deleting the item from DynamoDB table: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting the item from DynamoDB table: {e}")
        }

    # Return a success message
    print(f"Item with db_name {db_name} deleted successfully")
    return {
        'statusCode': 200,
        'body': json.dumps(f"Item with db_name {db_name} deleted successfully")
    }
