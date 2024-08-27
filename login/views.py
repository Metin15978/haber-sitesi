from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login,logout
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        login_info = request.POST.get('username')
        password = request.POST.get('password')
        
        if not login_info or not password:
            messages.error(request, 'Kullanıcı adı ve şifre gereklidir.')
            return render(request, 'login/login.html')
        
        try:
            user_mail = User.objects.get(email=login_info)
            user = authenticate(request, username=user_mail.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=login_info, password=password)
        
        if user is not None:
            try:
                customer = Reader.objects.get(user=user)
                auth_login(request, user)
                return redirect('home')
            except Reader.DoesNotExist:
                try: 
                    staff = Author.objects.get(user=user)
                    auth_login(request, user)
                    return redirect('home')
                except Author.DoesNotExist:
                    messages.error(request, 'Kullanıcı mevcut ancak Müşteri veya Personel değil.')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış!')
    return render(request, 'login/login.html' )
    

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(first_name)
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Kullanıcı adı zaten mevcut!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email zaten mevcut!')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                print(user.id)
                customer = Reader.objects.create(user=user, phone=phone)
                customer.save()
                print(customer)
                auth_login(request, user)
                return redirect('login')  # Kayıt başarılıysa yönlendirilecek sayfa
        else:
            messages.error(request, 'Şifreler eşleşmiyor!')
    return render(request, 'login/login.html')


def userlogout(request):
    logout(request)
    return redirect('home')
