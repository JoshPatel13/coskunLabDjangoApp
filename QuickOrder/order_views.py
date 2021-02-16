from django.http import JsonResponse
from django.shortcuts import render
from django.http import Http404 
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import OrderSerializer
from .models import Order
from .database_abstraction import getAllOrderObjects
from .database_abstraction import getOrderObject
from .database_abstraction import updateOrderName
from .message_views import getApproval


# Called on Submit Request
@api_view(['POST'])
def addOrder(request):
    serializer = OrderSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        getApproval(request._request, serializer.data.get("order_id"), serializer.data.get("item_id"))
        updateOrderName(serializer.data.get("order_id"), serializer.data.get("item_id"))
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# View Order Table on frontend side
@api_view(['GET'])
def getOrders(request):
    try:
        items = getAllOrderObjects()
        serializer = OrderSerializer(items, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def deleteOrder(request, order_id):
    try: 
        item = getOrderObject(order_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)

