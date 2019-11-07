from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, 'mvp/home.html')


def signin(request):
    return render(request, 'mvp/signin.html')


def signup(request):
    return render(request, 'mvp/signup.html')
