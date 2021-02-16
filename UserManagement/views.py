from django.shortcuts import render

import json

from .models import User
from .models import Research
from .models import Dashboard


from .serializers import ResearchSerializer
from .serializers import UserSerializer
from .serializers import DashboardSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['DELETE'])
def softDeleteUser(request):
    body_unicode = request.body.decode('utf-8')
    try:
        user_id = int(request.GET.get("user_id"))
        user = User.objects.get(id = user_id)
        user.is_deleted = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteUser(request):
    body_unicode = request.body.decode('utf-8')
    try:
        user_id = int(request.GET.get("user_id"))
        user = User.objects.get(id = user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUsers(request):
    body_unicode = request.body.decode('utf-8')
    try:
        user_id = int(request.GET.get("user_id"))
        user = User.objects.get(id = user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except:
        users = User.objects.filter(is_deleted = False).order_by('name')
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)


@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def updateUser(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        user_id = body_data["user_id"]

        if ("email" in body_data.keys()):
            newEmail = body_data["email"]
            User.objects.filter(pk = user_id).update(email=newEmail)
        if ("phone_number" in body_data.keys()):
            newPhone_Number = body_data["phone_number"]
            User.objects.filter(pk = user_id).update(phone_number=newPhone_Number)
        if ("name" in body_data.keys()):
            newName = body_data["name"]
            User.objects.filter(pk = user_id).update(name=newName)
        user = User.objects.get(pk = user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addResearch(request):
    serializer = ResearchSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def getResearch(request):
    research = Research.objects.all()
    serializer = ResearchSerializer(research, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addResearchtoDashboard(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    userID = body_data["user_id"]
    researchID = body_data["research_id"]
    user = User.objects.get(id = userID)
    research = Research.objects.get(id = researchID)

    dashboard = Dashboard(user=user,research=research)
    dashboard.save()
    serializer = DashboardSerializer(dashboard)
    return Response(serializer.data)

@api_view(['GET'])
def getAllDashboards(request):
        dashboard = Dashboard.objects.all()
        serializer = DashboardSerializer(dashboard, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def getDashboard(request):
    # body_unicode = request.body.decode('utf-8')
    # body_data = json.loads(body_unicode)
    # user_id = body_data["user_id"]
    user_id = int(request.GET.get("user_id"))

    dashboard = Dashboard.objects.filter(user_id = user_id)

    wanted_research = set()

    nothing_added = True

    for research in Research.objects.all():
        for pos in dashboard:
            if research == pos.research:
                nothing_added = False
                wanted_research.add(research.id)

    if nothing_added:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        research = Research.objects.filter(pk__in = wanted_research)
        serializer = ResearchSerializer(research, many = True)
        return Response(serializer.data)

@api_view(['DELETE'])
def deleteResearchfromDashboard(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        user_id = body_data["user_id"]
        research_id = body_data["research_id"]

        dashboard = Dashboard.objects.filter(id = user_id)
        dashboard = dashboard.filter(id = research_id)
        if (not dashboard):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            dashboard.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
