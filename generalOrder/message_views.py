from slack import WebClient

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from django.shortcuts import redirect

from .models import GenOrderTable

from .database_abstractions import getGeneralOrderObject

from .messages import slackMessage
from .messages import slackApprove
from .messages import slackDecline

from . import constants
from . import secret_keys

from mailjet_rest import Client
import os





slackClient = WebClient(secret_keys.slack_key)



@api_view(['POST'])
def getApproval(request, order_id, item_id):
    slackClient.chat_postMessage(
        channel = 'G0169TH7561',
        blocks = slackMessage(order_id)
    )

    
    return Response(status = status.HTTP_200_OK )


@api_view(['POST'])
def AdminApprove(request):

    check = json.loads(request.POST.get("payload"))
    buttonName = check.get("actions")[0].get("text").get("text")
    order_id = check.get("actions")[0].get("block_id").split(":")[1]


    if buttonName == 'Approve':
        updateOrderStatus("Approved", order_id)
        slackClient.chat_update(
            channel = "G0169TH7561",
            ts = check.get("message").get("ts"),
            blocks = slackApprove(order_id)
        )

        data = email(order_id)
        result = mailjet.send.create(data=data)

    if buttonName == 'Decline':
        updateOrderStatus("Declined", order_id)
        slackClient.chat_update(
            channel = "G0169TH7561",
            ts = check.get("message").get("ts"),
            blocks = slackDecline(order_id)
        )

    return Response(status = status.HTTP_200_OK)



