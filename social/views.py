from django.shortcuts import render

# Create your views here.
def index(request):
    return 'Hello From the Landing Page(index)'

def home(request):
    return 'Hello From the Home Page'