from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, LoginUserForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    return HttpResponse('Hello From Home Page')

def signupUser(request):
    form = UserRegistrationForm()
    context = {'form': form}

    if request.user.is_authenticated:
        return redirect(index)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if User.objects.filter(username=user.username.lower()).exists():
                messages.error(
                    request, f'A User with the username, {user.username}, already exists.')
            elif User.objects.filter(email=user.email.lower()).exists():
                messages.error(request,
                               f'A User with the email, {user.email}, already exists.')
            else:
                user.email = user.email.lower()
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect(index)
    return render(request, 'signup.html', context)

def loginUser(request):
    form = LoginUserForm()
    context = {'form': form}

    if request.user.is_authenticated:
        return redirect(index)

    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            try:
                user_exist = User.objects.get(username=username)
                if user_exist:
                    user = authenticate(
                        request, username=username, password=password)
                    if user:
                        login(request, user)
                        return redirect(index)
                    else:
                        messages.error(request, 'Invalid username or password')
            except:
                messages.error(request, 'User does not exist, sign-up')

    return render(request, 'login.html', context)
