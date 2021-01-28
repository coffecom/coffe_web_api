from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
import json
from .serializers import ItemSerializer, DayScheduleSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, DaySchedule, Receipt

#ITEMS

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated]) #IsAuthenticated добавить группы пользователей и ссылки на них в моделях
def getAllItems(request):
    items = Item.objects.all().order_by('id')
    serializer = ItemSerializer(items, many = True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def createItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def deleteItemByName(request, name):
    if request.user.groups.filter(name = 'Managers').exists():
        try:
            item = Item.objects.get(name=name)
        except ObjectDoesNotExist  as e: return Response({"Error":"Wrong item name"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response({"Done":"Item deleted"}, status=status.HTTP_200_OK)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def deleteItemById(request, id):
    if request.user.groups.filter(name = 'Managers').exists():
        try:
            item = Item.objects.get(id=id)
        except ObjectDoesNotExist  as e: return Response({"Error":"Wrong item id"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response({"Done":"Item deleted"}, status=status.HTTP_200_OK)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def getItemByName(request, name):
    try:
        item = Item.objects.get(name=name)
    except ObjectDoesNotExist  as e: return Response({"Error":"Wrong item name"}, status=status.HTTP_404_NOT_FOUND)
    serializer= ItemSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def getItemById(request, id):
    try:
        item = Item.objects.get(id=id)
    except ObjectDoesNotExist  as e: return Response({"Error":"Wrong item id"}, status=status.HTTP_404_NOT_FOUND)
    serializer= ItemSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def patcItemByName(request, name):
    if request.user.groups.filter(name = 'Managers').exists():
        try: item = Item.objects.get(name=name)
        except ObjectDoesNotExist  as e: return Response({"Error":"Wrong item name"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': 'Bad JSON'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def patcItemById(request, id):
    if request.user.groups.filter(name = 'Managers').exists():
        try: item = Item.objects.get(id=id)
        except ObjectDoesNotExist  as e: return Response({"Error":"Wrong item id"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': 'Bad JSON'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)

#USERS

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAdminUser])
def createManager(request):
    userName = request.data['username']
    userPass = request.data['password']
    userMail = request.data['email']

    user = User.objects.create_user(username=userName,
                                 email=userMail,
                                 password=userPass)

    my_group = Group.objects.get(name='Managers') 
    my_group.user_set.add(user)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def createBarista(request):
    if request.user.groups.filter(name = 'Managers').exists():
        userName = request.data['username']
        userPass = request.data['password']
        userMail = request.data['email']

        user = User.objects.create_user(username=userName,
                                     email=userMail,
                                     password=userPass)

        my_group = Group.objects.get(name='Baristas') 
        my_group.user_set.add(user)
        return Response({userName: 'barista is created'}, status=status.HTTP_200_OK)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def authentication(request, format=None):
    userName = request.data['username']
    userPass = request.data['password']
    if userName == None or userPass == None: Response({'error': 'Please enter username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=userName, password=userPass)

    if not user: return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)


#DAY SHEDULE

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def getDayShechuleById(request, id):
    try:
        shechule = DaySchedule.objects.get(id=id)
    except ObjectDoesNotExist  as e: return Response({"Error":"Wrong day schedule id"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DayScheduleSerializer(shechule)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def getAllDayShechules(request):
    try:
        shechule = DaySchedule.objects.all().order_by('id')
    except ObjectDoesNotExist  as e: return Response({"Error":"Wrong day schedule id"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DayScheduleSerializer(shechule, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def getDayShechuleByDate(request, date):
    # print("DATE", date)
    try: shechule = DaySchedule.objects.get(date=date)
    except ObjectDoesNotExist  as e: return Response({"Error":"Wrong day schedule id"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DayScheduleSerializer(shechule)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def createDayShechule(request):
    if request.user.groups.filter(name = 'Managers').exists():
        serializer = DayScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def patchDayShechuleByDate(request, date):
    if request.user.groups.filter(name = 'Managers').exists():
        try: shechule = DaySchedule.objects.get(date=date)
        except ObjectDoesNotExist  as e: return Response({"Error":"Wrong day schedule date"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DayScheduleSerializer(shechule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': 'Bad JSON'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def patchDayShechuleById(request, id):
    if request.user.groups.filter(name = 'Managers').exists():
        try: shechule = DaySchedule.objects.get(id=id)
        except ObjectDoesNotExist: return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DayScheduleSerializer(shechule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': 'Bad JSON'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'User is not authorized or is not a Manager'}, status=status.HTTP_401_UNAUTHORIZED)


#RECIEPT get patch delete 




#RECIEPT ITEM

