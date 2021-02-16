from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import LevelReading, Livestream
from .serializers import LevelReadingSerializer, LivestreamSerializer


# Create your views here.

@api_view(['GET'])
def get_latest(request):
    readings = LevelReading.objects.all()
    if not readings:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        latest_reading = readings.order_by("-id")[0]
        serializer = LevelReadingSerializer(latest_reading)
        return Response(serializer.data)


@api_view(['GET'])
def get_livestreams(request):
    livestreams = Livestream.objects.all()
    serializer = LivestreamSerializer(livestreams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_livestream(request):
    serializer = LivestreamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET'])
def delete_livestream(request, id):
    try: 
        stream = Livestream.objects.get(id = id)
        stream.delete()    
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)
