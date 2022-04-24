from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer

from jutshirt_app.models import CustomUser, Admin, Customer, Products, Oder
import uuid
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from jutshirt_app.EmailBackEnd import EmailBackEnd
import requests
# settings
from django.conf import settings

import pyrebase
import os

config = {
    "apiKey": "AIzaSyBKHJcfyIlRD4va5PfYdS108IdNOV7mYXY",
    "authDomain": "biee-ju.firebaseapp.com",
    "projectId": "biee-ju",
    "storageBucket": "biee-ju.appspot.com",
    "messagingSenderId": "656841323932",
    "appId": "1:656841323932:web:2a2544aadd67433a9ac459",
    "measurementId": "G-DEHDJS4RX4",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


# Admin Home Dashboard
class Admin_home(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            product_count = Products.objects.all().count()
            customer_count = Customer.objects.all().count()
            order_count = Oder.objects.all().count()


            context = {
                'product_count': product_count,
                'customer_count': customer_count,
                'order_count': order_count,
            }

            return render(request, 'admin/admin_home.html', context)
        else:
            return redirect('login')



