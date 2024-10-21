def handler(event, context):
    print(f"Received random number: {event['random_number']}")
    return event
