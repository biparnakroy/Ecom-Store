from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from jutshirt_app.EmailBackEnd import EmailBackEnd

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
import uuid
from jutshirt_app.models import CustomUser, Admin, Customer
# csrf_exempt
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                #return HttpResponse("Admin Login")
                return redirect('admin_home')

            elif user_type == '2':
                return HttpResponse("Staff Login")
                # return redirect('customer_home')

            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def signup_page(request):
    return render(request, 'signup.html')

# do signup


def do_signup(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        year = request.POST.get('year')
        phone = request.POST.get('phone')
        username =  uuid.uuid4()

        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
        user.customer.customer_year = year
        user.customer.customer_phone = phone
        user.customer.uuid = username
        user.save()

        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        user_type = user.user_type
        login(request, user)
        if user_type == '1':
            #return HttpResponse("Admin Login")
            return redirect('login')

        elif user_type == '2':
            return HttpResponse("Customer Login")
            # return redirect('customer_home')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
