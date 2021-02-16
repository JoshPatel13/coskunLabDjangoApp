from .database_abstraction import getInventoryObject
from .database_abstraction import getOrderObject
from .database_abstraction import getUserEmail

def slackMessage(order_id, item_id):
    blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "NEW ORDER REQUEST \n\n Item Name: " 
                    + getInventoryObject(item_id).item_name 
                    + "\n Requested Quantity: " + str(getOrderObject(order_id).requested_quantity)
                    + "\n Ordered By: " + str(getUserEmail(getOrderObject(order_id).user.id))
                    + "\n Order Date: " + str(getOrderObject(order_id).order_date)
                }
            },
            {
                "type": "actions",
                "block_id": "coskun" + ":" + str(item_id) + ":" + str(order_id),
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Approve"
                        },
                        "action_id": "Approve",
                        "style": "primary",
                        "value": "aprrove_button"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Decline"
                        },
                        "action_id": "Decline",
                        "style": "danger",
                        "value": "decline_button"
                    }
                    
                ]
            }
        ]

    return blocks


def slackApprove(order_id, item_id):
    blocks = [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Item Name: " 
                    + getInventoryObject(item_id).item_name 
                    + "\n Requested Quantity: " + str(getOrderObject(order_id).requested_quantity)
                    + "\n Ordered By: " + str(getUserEmail(getOrderObject(order_id).user.id))
                    + "\n Order Date: " + str(getOrderObject(order_id).order_date)
                    + "\n\n ORDER APPROVED"
                }
            }]
    return blocks

def email(order_id, item_id):
    data = {
            'Messages': [
                    {
                        "From": {
                            "Email": "coskunlab@gatech.edu",
                            "Name": "Coskun Lab"
                        },
                        "To": [
                            {
                                "Email": "coskunlaboratory@gmail.com",
                                "Name": "Finance"
                            }
                        ],
                        "TemplateID": 1476639,
                        "TemplateLanguage": True,
                        "Subject": "New Order Request",
                        "Variables": {
                            "item_name": getInventoryObject(item_id).item_name ,
                            "requested_quantity": str(getOrderObject(order_id).requested_quantity),
                            "user_name": str(getUserEmail(getOrderObject(order_id).user.id)),
                            "order_date":  str(getOrderObject(order_id).order_date),
                            "order_id": str(order_id),
                            "item_id": str(item_id)
                        }
                    }
                ]
        }
    return data

def slackDecline(order_id, item_id):
    blocks = [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Item Name: " 
                    + getInventoryObject(item_id).item_name 
                    + "\n Requested Quantity: " + str(getOrderObject(order_id).requested_quantity)
                    + "\n Ordered By: " + str(getUserEmail(getOrderObject(order_id).user.id))
                    + "\n Order Date: " + str(getOrderObject(order_id).order_date)
                    + "\n\n ORDER DECLINED"
                }
            }]
    return blocks