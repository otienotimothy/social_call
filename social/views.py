from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, LoginUserForm, CreatePostForm, EditProfileForm, CreateCommentForm
from .models import  Profile, Post

# Create your views here.
def index(request):

    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    form = CreatePostForm()
    commentForm = CreateCommentForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by_id = request.user.id
            post.save()
            messages.success(request, 'Your Post was Created Successfully')
        else:
            messages.error(request, 'An Error occurred while uploading your image')

    try:
        posts = Post.objects.all()
    except:
        messages.error(request, 'An Error occured while fetching Posts')
    
    context = {'form': form, 'posts':posts, 'commentInput': commentForm}
    return render(request, 'home.html', context)

@login_required(login_url='login')
def loadProfile(request, username):


    if username != request.user.username:
        logout(request)
        return redirect('login')

    try:
        userProfile = User.objects.get(username=username)
        posts = Post.objects.filter(posted_by__username=username)
    except:
        messages.error('An error occurred while loading Profile...')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
    
    form = EditProfileForm()
    context = {'form':form, 'profile': userProfile, 'posts':posts}
    return render(request, 'profile.html', context)

# User Creation and Authentication 
# 1. User Creation
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
                userProfile = Profile(user=user)
                userProfile.save()
                login(request, user)
                return redirect(home)
    return render(request, 'signup.html', context)

# 2. User Authentication
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

@login_required(login_url='login')
def addComment(request, postId):
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            commentObj = form.save(commit=False)
            commentObj.commented_post_id = postId
            commentObj.commentor_id = request.user.id
            commentObj.save()
        else:
            messages.error(request, 'An error occurred while posting your comment...')

    return redirect(home)

@login_required(login_url='login')
def deletePost(request, postId):
    try:
        Post.objects.get(pk=postId).delete()
    except:
        messages.error(request, 'An error occured while tring to delete the post...')

    return redirect('profile')