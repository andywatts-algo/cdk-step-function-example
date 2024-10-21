import random

def handler(event, context):
    return {"random_number": random.randint(1, 100)}
