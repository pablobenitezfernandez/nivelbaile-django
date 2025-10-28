from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def nivel(request):
    return render(request, 'nivel.html')
