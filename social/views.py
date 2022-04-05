from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, LoginUserForm, CreatePostForm

# Create your views here.
def index(request):

    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    form = CreatePostForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CreatePostForm(request.Post, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by_id = request.user.id
            post.save()
            messages.success(request, 'Your Post was Created Successfully')
        else:
            messages.error(request, 'An Error occurred while uploading your image')

    return render(request, 'home.html', context)

@login_required
def loadProfile(request, username):
    return render(request, 'profile.html')

def signupUser(request):
    form = UserRegistrationForm()
    context = {'form': form}

    if request.user.is_authenticated:
        return redirect(home)

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
                return redirect(home)
    return render(request, 'signup.html', context)

def loginUser(request):
    form = LoginUserForm()
    context = {'form': form}

    if request.user.is_authenticated:
        return redirect(home)

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
                        return redirect(home)
                    else:
                        messages.error(request, 'Invalid username or password')
            except:
                messages.error(request, 'User does not exist, sign-up')

    return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect(loginUser)
