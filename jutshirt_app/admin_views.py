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

from jutshirt_app.models import CustomUser, Admin, Customer, Products, Order
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


# Admin Profile View
class AdminProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        admin = Admin.objects.get(user=request.user)
        context = {
            'admin': admin,
        }
        return render(request, 'admin/admin_profile.html', context)

# Admin Profile Edit
class AdminProfileEditView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        admin = Admin.objects.get(user=request.user)
        context = {
            'admin': admin,
        }
        return render(request, 'admin/admin_profile_edit.html', context)

    def post(self, request):
        admin = Admin.objects.get(user=request.user)
        admin.user.first_name = request.POST['first_name']
        admin.user.last_name = request.POST['last_name']
        admin.user.email = request.POST['email']
        password = request.POST['password']

        # changing password if not empty
        if password != '':
            # setting new password
            admin.user.set_password(password)
            admin.user.save()
            # re authenticating user with new password and emailbackend
            user = EmailBackEnd.authenticate(request, username=admin.user.email, password=password)
            if user is not None:
                login(request, user)
            else :
                return redirect('login')
            #user = authenticate(username=admin.user.username, password=password)

        admin.user.save()
        admin.save()

        return redirect('admin_profile')


# Admin Home Dashboard
class Admin_home(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            product_count = Products.objects.all().count()
            customer_count = Customer.objects.all().count()
            order_count = Order.objects.all().count()


            context = {
                'product_count': product_count,
                'customer_count': customer_count,
                'order_count': order_count,
            }

            return render(request, 'admin/admin_home.html', context)
        else:
            return redirect('login')

# Add products

class Admin_add_products(APIView):
    permissions_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            return render(request, 'admin/admin_add_products.html')
        else:
            return redirect('login')

    def post(self,request):
        if request.user.user_type == '1':
            prod_name = request.POST.get('prod_name')
            prod_type = request.POST.get('prod_type')
            prod_des = request.POST.get('prod_des')
            prod_pic = request.POST.get('prod_pic')
            prod_price = request.POST.get('prod_price')

            print(prod_name)

            # create a new product
            if prod_name and prod_type and prod_des and prod_pic and prod_price :
                product = Products.objects.create(uuid=uuid.uuid4(),name=prod_name, product_type=prod_type, description=prod_des,picture=prod_pic,price=prod_price)
                messages.success(request, 'Department Created Successfully')
                return redirect('admin_home')
            else:
                return redirect('admin_add_products')
        else:
            return redirect('login')

# manage products
class Manage_products(APIView):
    permissions_classes = (IsAuthenticated,)

    def get(self,request):
        products = Products.objects.all()
        context={
            'products' : products,
        }
        return render(request,'admin/admin_manage_products.html', context)

# view products
class View_products(APIView):
    permissions_classes = (IsAuthenticated,)

    def get(self,request,prod_uuid):
        if request.user.user_type == '1':
            prod = Products.objects.get(uuid=prod_uuid)
            context = {
                'prod': prod,
            }
            return render(request, 'admin/admin_view_prod.html', context)
        else:
            return redirect('login')

# edit products
class Edit_products(APIView):
    permissions_classes = (IsAuthenticated,)

    def get(self,request, prod_uuid):
        if request.user.user_type == '1':
            prod = Products.objects.get(uuid=prod_uuid)
            context = {
                'prod': prod,
            }
            return render(request, 'admin/admin_edit_prod.html', context)
        else:
            return redirect('login')

    def post(self,request,prod_uuid):
        if request.user.user_type == '1':
            prod = Products.objects.get(uuid=prod_uuid)
            prod_name = request.POST.get('prod_name')
            prod_type = request.POST.get('prod_type')
            prod_des = request.POST.get('prod_des')
            prod_pic = request.POST.get('prod_pic')
            prod_price = request.POST.get('prod_price')

            if prod_name and prod_type and prod_des and prod_pic and prod_price :
                prod.name = prod_name
                prod.product_type = prod_type
                prod.description = prod_des
                prod.picture = prod_pic
                prod.price = prod_price
                prod.save()
                return redirect('admin_manage_products')
            else:
                return redirect('admin_manage_products')
        else:
            return redirect('login')
    
# delete product
class Delete_prod(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, prod_uuid):
        if request.user.user_type == '1':
            prod = Products.objects.get(uuid=prod_uuid)
            prod.delete()
            return redirect('admin_manage_products')
        else:
            return redirect('login')
    

# Manage Customers

class Manage_customers(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '1':
            customer = Customer.objects.all()
            context = {
                'customers' : customer,
            }
            return render(request, 'admin/admin_manage_customer.html', context)
        else:
            return redirect('login')

# View Customers

class View_customers(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,uuid):
        if request.user.user_type == '1':
            customer = Customer.objects.get(customer_uuid=uuid)
            cart = customer.cart
            context={
                'customer' : customer,
                'cart' : "",
            }
            if cart:
                cart = cart.split('|')
                items=[]
                for item in cart:
                    if len(item):
                        current_cart  = item.split(',')
                        current_cart[0]= current_cart[0][1:]
                        current_cart[-1] = current_cart[-1][:-1]
                        current_item = {
                            'prod' : Products.objects.get(uuid= current_cart[0]),
                            'size' : current_cart[1],
                            'qnt' : current_cart[2],
                        }
                        items.append(current_item)
                        context={
                            'customer' : customer,
                            'cart' : items,
                        }
                    else:
                        pass
                   
            return render(request,'admin/admin_view_customer.html', context)
        else :
            return redirect('login')

#=======================Edit Customer=====================

class Edit_customer(APIView):
    def get(self, request,uuid):
        if request.user.user_type == '1':
            customer = Customer.objects.get(customer_uuid=uuid)
            context={
                'customer' : customer,
            }
            return render(request,'admin/admin_edit_customer.html', context)
        else:
            return redirect('login')
    



#=====================Form Validation Function=====================

#checking if the username is already taken
class Username_check(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        username = request.POST.get('username')
        user = CustomUser.objects.filter(username=username).exists()
        if user:
            return JsonResponse({'status': 'taken'})
        else:
            return JsonResponse({'status': 'available'})


#checking if the email is already taken
class Email_check(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return JsonResponse({'status': 'taken'})
        else:
            return JsonResponse({'status': 'available'})





