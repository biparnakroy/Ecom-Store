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

# Add item to cart
class Add_to_cart(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def post(self, request):
        if request.user.user_type == '2':
            product = request.data['product_uuid']
            size = request.data['size']
            quantity = request.data['qty']

            # Check if product is already in cart anf update quantity
            new_cart=""
            cart = request.user.customer.cart
            found = False
            if cart:
                cart = cart.split('|')
                cart= cart[:-1]
                for item in cart:
                    current_cart  = item.split(',')
                    current_cart[0]= current_cart[0][1:]
                    current_cart[-1] = current_cart[-1][:-1]
                    if current_cart[0] == product and current_cart[1] == size:
                        current_cart[2] = str(int(current_cart[2]) + int(quantity))
                        found = True
                    new_cart += '['+ current_cart[0] + ',' + current_cart[1] + ',' + current_cart[2] + ']|'
                if not found:
                    new_cart += '['+ product + ',' + size + ',' + quantity + ']|'      
            else:
                new_cart = '[' + product + ',' + size + ',' + quantity + ']|'

            request.user.customer.cart = new_cart

            request.user.customer.save()
            return HttpResponse('success')
        else:
            return redirect('login')

# Delete item from cart
class Delete_from_cart(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request,uuid,size):
        if request.user.user_type == '2':
            product = uuid

            # Check if product is already in cart anf update quantity
            new_cart=""
            cart = request.user.customer.cart
            found = False
            if cart:
                cart = cart.split('|')
                cart= cart[:-1]
                for item in cart:
                    current_cart  = item.split(',')
                    current_cart[0]= current_cart[0][1:]
                    current_cart[-1] = current_cart[-1][:-1]
                    if current_cart[0] == product and current_cart[1] == size:
                       pass
                    else:
                        new_cart += '['+ current_cart[0] + ',' + current_cart[1] + ',' + current_cart[2] + ']|'
                request.user.customer.cart = new_cart
            else:
                pass
            request.user.customer.save()
            return redirect('customer_cart')
        else:
            return redirect('login')

# Customer Cart Page
class Customer_cart(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '2':
            cart = request.user.customer.cart
            context={
                'cart' : "",
            }
            total=0
            if cart:
                cart = cart.split('|')
                items=[]
                for item in cart:
                    if len(item):
                        current_cart  = item.split(',')
                        current_cart[0]= current_cart[0][1:]
                        current_cart[-1] = current_cart[-1][:-1]
                        product = Products.objects.get(uuid=current_cart[0])
                        total += int(current_cart[2]) * int(product.price)

                        current_item = {
                            'prod' : product,
                            'size' : current_cart[1],
                            'qnt' : current_cart[2],
                        }
                        items.append(current_item)
                        context={
                            'cart' : items,
                            'total' : str(total),
                        }
                    else:
                        pass

            return render(request, 'customer/customer_cart.html', context)
        else:
            return redirect('login')


# Customer Checkout Page
class Customer_checkout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '2':
            cart = request.user.customer.cart
            context={
                'cart' : "",
            }
            total=0
            if cart:
                cart = cart.split('|')
                items=[]
                for item in cart:
                    if len(item):
                        current_cart  = item.split(',')
                        current_cart[0]= current_cart[0][1:]
                        current_cart[-1] = current_cart[-1][:-1]
                        product = Products.objects.get(uuid=current_cart[0])
                        total += int(current_cart[2]) * int(product.price)

                        current_item = {
                            'prod' : product,
                            'size' : current_cart[1],
                            'qnt' : current_cart[2],
                        }
                        items.append(current_item)
                        context={
                            'cart' : items,
                            'total' : str(total),
                        }
                    else:
                        pass

            return render(request, 'customer/customer_checkout.html', context)
        else:
            return redirect('login')



    
