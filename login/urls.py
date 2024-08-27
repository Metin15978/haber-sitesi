from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.userlogout, name="logout"),
]