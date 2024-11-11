# bidding_manager.py
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError

def place_bid(dynamodb, property_id, buyer_id, bid_amount):
    """
    Places a new bid on a property.

    :param dynamodb: The DynamoDB resource client passed from app.py.
    :param property_id: The ID of the property being bid on.
    :param buyer_id: The ID of the buyer placing the bid.
    :param bid_amount: The bid amount.
    :return: The bid ID or error message.
    """
    bids_table = dynamodb.Table('Bids')
    properties_table = dynamodb.Table('Properties')
    
    try:
        # Ensure the bid is higher than the current highest bid
        highest_bid = get_highest_bid(dynamodb, property_id)
        if bid_amount <= highest_bid:
            return "Bid amount must be higher than the current highest bid."

        # Place the new bid
        bid_id = str(uuid.uuid4())
        bids_table.put_item(Item={
            'bid_id': bid_id,
            'property_id': property_id,
            'buyer_id': buyer_id,
            'bid_amount': str(bid_amount)  # Store as string for DynamoDB compatibility
        })
        return bid_id  # Return the new bid's ID

    except Exception as e:
        return str(e)

def get_bids_for_property(dynamodb, property_id):
    """
    Retrieves all bids placed on a property.

    :param dynamodb: The DynamoDB resource client passed from app.py.
    :param property_id: The ID of the property.
    :return: A list of bids.
    """
    try:
        bids_table = dynamodb.Table('Bids')
        response = bids_table.scan(
            FilterExpression="property_id = :property_id",
            ExpressionAttributeValues={":property_id": property_id}
        )
        return response.get('Items', [])
    except Exception as e:
        return str(e)

def get_highest_bid(dynamodb, property_id):
    """
    Retrieves the highest bid for a property.

    :param dynamodb: The DynamoDB resource client passed from app.py.
    :param property_id: The ID of the property.
    :return: The highest bid amount.
    """
    bids = get_bids_for_property(dynamodb, property_id)
    if not bids:
        # If no bids, return starting price or 0 if not set
        return Decimal(0)
    
    # Sort bids by bid_amount and return the highest
    sorted_bids = sorted(bids, key=lambda x: Decimal(x['bid_amount']), reverse=True)
    return Decimal(sorted_bids[0]['bid_amount'])

def accept_bid(dynamodb, bid_id, property_id):
    try:
        bids_table = dynamodb.Table('Bids')
        properties_table = dynamodb.Table('Properties')

        # Fetch the bid details
        bid = bids_table.get_item(Key={'bid_id': bid_id}).get('Item')
        if not bid:
            return "Bid not found."
        
        # Fetch property details
        property_item = properties_table.get_item(Key={'property_id': property_id}).get('Item')
        if not property_item:
            return "Property not found."

        # Mark the bid as accepted and update the property status to sold
        bid['accepted'] = True
        bids_table.put_item(Item=bid)
        properties_table.update_item(
            Key={'property_id': property_id},
            UpdateExpression="SET sold = :sold",
            ExpressionAttributeValues={':sold': True}
        )

        # Return a success message with details
        return {
            "message": f"Congratulations! Your bid of ${bid['bid_amount']} for the property '{property_item['title']}' was accepted.",
            "buyer_id": bid['buyer_id']
        }
    except Exception as e:
        return str(e)