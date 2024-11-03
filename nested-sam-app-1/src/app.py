import json

def lambda_handler(event, context):
    print('Received event:', json.dumps(event))
    print('S3 bucket:', event['detail']['bucket']['name'])
    print('S3 object:', event['detail']['object']['key'])
    # Add your processing logic here
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed S3 event')
    }