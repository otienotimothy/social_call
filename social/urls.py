from unicodedata import name
from django.urls import path

from .views import index, home, signupUser, loginUser

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('signup/', signupUser, name='signup' ),
    path('login/', loginUser, name='login')
]