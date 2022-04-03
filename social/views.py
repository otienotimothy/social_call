from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserCreationForm, LoginUserForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return HttpResponse('Hello From Home Page')

def signupUser(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'signup.html', context)

def loginUser(request):
    form = LoginUserForm()
    context = {'form': form}
    return render(request, 'login.html', context)
