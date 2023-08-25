from django.shortcuts import render
from datetime import datetime, timedelta
from multiprocessing import AuthenticationError
import jwt
from django.shortcuts import render
from django.http import JsonResponse
from django.http.request import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from .models import User, application, job
from .serializers import UserLoginSerializer, JobSerializer, application_Serializer, UserSerializer


@api_view(['POST'])
def register(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def registerMul(request):
    serializer = UserLoginSerializer(data=request.data,many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

def registerM(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.filter(email=email).first()
    isDofa =False
    if user == None:
        raise AuthenticationFailed('User not found')
    if user.check_password(password) == False:
        raise AuthenticationFailed("incorrect password")
    if (user.cse_Acess and user.cce_Acess and user.ece_Acess and user.mec_Acess):
        isDofa = True
    
    payload = {
        'id': user.id,  
        'name': user.name,
        'email': user.email,
        'exp': datetime.utcnow()+timedelta(minutes=180),
        'iat': datetime.utcnow(),
        'isDofa': isDofa,
        'isCse':user.cse_Acess,
        'isEse':user.ece_Acess,
        'isCce':user.cce_Acess,
        'isMec':user.mec_Acess
    }

    token = jwt.encode(payload=payload, key='secret', algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    decode = jwt.decode(token, 'secret', algorithms=['HS256'])
    response.data = {'jwt': token}
    return response



@api_view(['POST'])
def grant_Perms(request):
    
    email = request.data.get("email")
    user = User.objects.filter(email=email).first()
    user.cse_Acess = (request.data.get("cse") == "True")
    user.ece_Acess = (request.data.get("ece") == "True")
    user.cce_Acess = (request.data.get("cce") == "True")
    user.mec_Acess = (request.data.get("mec") == "True")
    user.save()
    return Response({"good": "response"})


def Decode(token):
    try:
        decode = jwt.decode(token, 'secret', algorithms=['HS256'])
        return decode
    except:
        return None


def authuser(request):  
    payload = Decode(request.query_params.get('jwt', "lol"))
    if payload == None:
        return None
    user = User.objects.get(pk=payload['id'])
    if user:
        return user
    else:

        return None


def authDofa(request):

    print(request.query_params.get('jwt', None))
    payload = Decode(request.query_params.get('jwt', "lol"))
    if payload == None:
        print("couldnt decode")
        return None  
    user = User.objects.get(pk=payload['id'])
    if user and user.cse_Acess and user.ece_Acess and user.cce_Acess and user.mec_Acess:
        return user
    else:
        print("No user")
        return None
def authAdmin(request):

    print(request.query_params.get('jwt', None))
    payload = Decode(request.query_params.get('jwt', "lol"))
    if payload == None:
        print("couldnt decode")
        return None  
    user = User.objects.get(pk=payload['id'])
    if user and (user.cse_Acess or user.ece_Acess or user.cce_Acess or user.mec_Acess):
        return user
    else:
        print("No user")
        return None

def authCse(request):

    print(request.query_params.get('jwt', None))
    payload = Decode(request.query_params.get('jwt', "lol"))
    if payload == None:
        print("couldnt decode")
        return None  
    user = User.objects.get(pk=payload['id'])
    if user and user.cse_Acess:
        return user
    else:
        print("No user")
        return None


def authCce(request):
    print(request.query_params.get('jwt', None))
    payload = Decode(request.query_params.get('jwt', "lol"))
    if payload == None:
        print("couldnt decode")
        return None  
    user = User.objects.get(pk=payload['id'])
    if user and user.cce_Acess:
        return user
    else:
        print("No user")
        return None


def authEce(request):
    print(request.query_params.get('jwt', None))
    payload = Decode(request.query_params.get('jwt', "lol"))
    if payload == None:
        print("couldnt decode")
        return None  
    user = User.objects.get(pk=payload['id'])
    if user and user.ece_Acess:
        return user
    else:
        print("No user")
        return None


def authMMe(request):
    print(request.query_params.get('jwt', None))
    payload = Decode(request.query_params.get('jwt', "lol"))
    if payload == None:
        print("couldnt decode")
        return None  
    user = User.objects.get(pk=payload['id'])
    if user and user.mec_Acess:
        return user
    else:
        print("No user")
        return None

@api_view(['POST'])
def logout(request):
    response=Response()
    response.delete_cookie('jwt')
    response.data={"success":"logout successful"}
    return response
    