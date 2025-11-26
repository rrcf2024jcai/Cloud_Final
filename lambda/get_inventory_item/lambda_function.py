import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        # Get the ID from the URL path parameters
        item_id = event['pathParameters']['id']
        
        # Query using the Partition Key (id)
        response = table.query(
            KeyConditionExpression=Key('id').eq(item_id)
        )
        
        items = response.get('Items', [])
        
        if not items:
            return {'statusCode': 404, 'body': json.dumps("Item not found")}
            
        # Return the first (and only) item found
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items[0], cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }