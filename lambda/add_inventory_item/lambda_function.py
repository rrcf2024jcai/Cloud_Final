import json
import boto3
import uuid 

# Connect to DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    print("Starting add_inventory_item function...")
    
    # Get the data sent from the user
    try:
        # Check if body exists
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps('No body found in request')
            }
            
        body_data = json.loads(event['body'])
        
        # Extract specific fields from the data
        item_name = body_data['name']
        item_desc = body_data['description']
        item_qty = int(body_data['qty'])     # Make sure it's a number
        item_price = str(body_data['price']) # Keep price as string or Decimal usually safely
        location_id = int(body_data['location_id'])
        
        # Generate a unique ID for this new item
        item_id = str(uuid.uuid4())
        
        # Create the item dictionary to save
        new_item = {
            'id': item_id,              # Partition Key
            'location_id': location_id, # Sort Key
            'name': item_name,
            'description': item_desc,
            'qty': item_qty,
            'price': item_price
        }
        
        print(f"Ready to add item: {new_item}")
        
        # Put the item into DynamoDB
        table.put_item(Item=new_item)
        
        # Return success message
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' 
            },
            'body': json.dumps(f"Success! Item added with ID: {item_id}")
        }

    except Exception as e:
        print(f"Something went wrong: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
