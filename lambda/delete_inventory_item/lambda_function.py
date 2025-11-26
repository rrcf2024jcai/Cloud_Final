import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        item_id = event['pathParameters']['id']
        
        # Find the item to get its location_id
        response = table.query(
            KeyConditionExpression=Key('id').eq(item_id)
        )
        items = response.get('Items', [])
        
        if not items:
            return {'statusCode': 404, 'body': json.dumps("Item not found, cannot delete")}
            
        # Get the location_id from the found item
        location_id = items[0]['location_id']
        
        # Delete the item using both keys
        table.delete_item(
            Key={
                'id': item_id,
                'location_id': location_id
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(f"Item {item_id} deleted successfully")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }