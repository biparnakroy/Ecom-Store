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

from jutshirt_app.models import CustomUser, Customer, Products, Order
import uuid
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from jutshirt_app.EmailBackEnd import EmailBackEnd
import requests
# settings
from django.conf import settings

# Customer Home Dashboard
class Customer_home(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '2':
            products = Products.objects.all()
            context = {
                'products' : products,
            }

            return render(request, 'customer/customer_home.html', context)
        else:
            return redirect('login')

# Customer Product Page
class Customer_product(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '2':
            products = Products.objects.all()
            context = {
                'products' : products,
            }

            return render(request, 'customer/customer_product.html', context)
        else:
            return redirect('login')

# Customer Product View Page
class Customer_product_view(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, uuid):
        if request.user.user_type == '2':
            product = Products.objects.get(uuid=uuid)
            context = {
                'product' : product,
            }

            return render(request, 'customer/customer_product_view.html', context)
        else:
            return redirect('login')


