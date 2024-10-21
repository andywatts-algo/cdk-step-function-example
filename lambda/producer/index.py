import boto3
import uuid
import os
import random

def handler(event, context):
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(os.environ['TABLE_NAME'])
    
    item = {
        'id': str(uuid.uuid4()),
        'random_number': random.randint(1, 100)
    }
    
    table.put_item(Item=item)
    return item
