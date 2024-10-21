import boto3
import os

def handler(event, context):
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(os.environ['TABLE_NAME'])
    
    response = table.get_item(Key={'id': event['id']})
    item = response['Item']
    
    print(f"Read item from DynamoDB: {item}")
    return item
