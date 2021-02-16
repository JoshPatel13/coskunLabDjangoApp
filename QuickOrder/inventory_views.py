from django.http import JsonResponse
from django.shortcuts import render
from django.http import Http404 
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import InventoryItemSerializer
from .models import InventoryItem
from .database_abstraction import getAllInventoryObjects
from .database_abstraction import getInventoryObject
from .database_abstraction import updateRefillNeeded

@api_view(['GET'])
def getInventory(request):
    try: 
        items = getAllInventoryObjects()
        serializer = InventoryItemSerializer(items, many = True)
        updateRefillNeeded(items)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getInventoryItem(request, item_id):
    try: 
        item = getInventoryObject(item_id)
        serializer = InventoryItemSerializer(item)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def addItem(request):
    serializer = InventoryItemSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateItem(request, item_id):
    item = getInventoryObject(item_id)
    serializer = InventoryItemSerializer(instance = item, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteItem(request, item_id):
    try: 
        item = getInventoryObject(item_id)
        item.is_deleted = True
        item.save()        
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)

