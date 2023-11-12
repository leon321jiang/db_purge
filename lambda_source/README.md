# DynamoDB Item Purge Lambda Function

## Description
This Lambda function performs the following actions:
1. Creates a backup of a specified DynamoDB table named 'onboarded_db_list'.
2. Deletes an item from the table, identified by the partition key 'db_name', provided as input to the Lambda.
3. Bcckup the deleted item to a table named 'Records_Deleted'

## Setup
Create lambda function and required iam roles and policy. 
The Lambda function requires the following IAM permissions:
```
dynamodb:CreateBackup
dynamodb:GetItem
dynamodb:DeleteItem
```
Make sure the execution role for the Lambda function has these permissions.

### Prerequisites
- AWS CLI already configured with appropriate permissions
- Python 3.8 environment for running and testing the Lambda function

### Deployment
Deploy the Lambda function using the AWS CLI or the AWS Management Console, ensuring the execution role has the necessary permissions.

### Invocation
Invoke the Lambda function by passing the 'db_name' in the event payload:
```bash
aws lambda invoke --function-name <FunctionName> --payload '{"db_name": "<value>"}' response.json