from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import EmailInput, TextInput, PasswordInput, FileInput, Select

from .models import Post, Profile, Comment


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class LoginUserForm(forms.Form):

    username = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control'}), max_length=100)
    password = forms.CharField(widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image_url']

        widgets = {
            'image_url': FileInput(attrs={'class': 'form-control mt-1'}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'firstName', 'lastName', 'bio', 'gender']
        widgets = {
            'avatar': FileInput(attrs={'class': 'form-control my-1'}),
            'firstName': TextInput(attrs={'class': 'form-control my-1'}),
            'lastName': TextInput(attrs={'class': 'form-control my-1'}),
            'bio': TextInput(attrs={'class': 'form-control my-1'}),
            'gender': Select(attrs={'class': 'form-select my-1'}),
        }


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': "Comment"}),
        }
