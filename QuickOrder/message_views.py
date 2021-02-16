from slack import WebClient

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from django.shortcuts import redirect

from .models import Order

from .database_abstraction import getOrderObject
from .database_abstraction import updateOrderStatus
from .database_abstraction import updateInventoryQuantity

from .messages import slackMessage
from .messages import slackApprove
from .messages import email
from .messages import slackDecline

from . import constants
from . import secret_keys

from mailjet_rest import Client
import os

# SLACK AND MAILJET CREDENTIALS

mailjet = Client(auth=(secret_keys.api_key, secret_keys.api_secret), version='v3.1')
slackClient = WebClient(secret_keys.slack_key)

@api_view(['POST'])
def getApproval(request, order_id, item_id):
    slackClient.chat_postMessage(
        channel = 'G0169TH7561',
        blocks = slackMessage(order_id, item_id)
    )

    return Response(status = status.HTTP_200_OK )

@api_view(['POST'])
def AdminApprove(request):
    check = json.loads(request.POST.get("payload"))
    buttonName = check.get("actions")[0].get("text").get("text")
    item_id = check.get("actions")[0].get("block_id").split(":")[1]
    order_id = check.get("actions")[0].get("block_id").split(":")[2]


    if buttonName == 'Approve':
        updateOrderStatus("Approved", order_id)
        slackClient.chat_update(
            channel = "G0169TH7561",
            ts = check.get("message").get("ts"),
            blocks = slackApprove(order_id, item_id)
        )

        data = email(order_id, item_id)
        result = mailjet.send.create(data=data)

    if buttonName == 'Decline':
        updateOrderStatus("Declined", order_id)
        slackClient.chat_update(
            channel = "G0169TH7561",
            ts = check.get("message").get("ts"),
            blocks = slackDecline(order_id, item_id)
        )

    return Response(status = status.HTTP_200_OK)

@api_view(['GET'])
def FinanceApprove(request, order_id):
    if (getOrderObject(order_id).status == "Approved"):
        updateOrderStatus("Ordered", order_id)
        return redirect(constants.URL + '/inventory/')
    return Response(status = status.HTTP_200_OK)

@api_view(['GET'])
def FinanceDeliver(request, order_id, item_id):
    if (getOrderObject(order_id).status == "Ordered"):
        updateOrderStatus("Delivered", order_id)
        updateInventoryQuantity(getOrderObject(order_id).requested_quantity, item_id)        
        return redirect(constants.URL + '/inventory/')
    return Response(status = status.HTTP_200_OK)

@api_view(['GET'])
def FinanceCancel(request, order_id):
    if (getOrderObject(order_id).status == "Approved" or getOrderObject(order_id).status == "Ordered"):
        updateOrderStatus("Cancelled", order_id)
        return redirect(constants.URL + '/inventory/')
    return Response(status = status.HTTP_200_OK)




