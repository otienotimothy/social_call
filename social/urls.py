from unicodedata import name
from django.urls import path

from .views import index, home, signupUser, loginUser, logoutUser, loadProfile, addComment

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('profile/<str:username>/', loadProfile, name='profile'),
    path('signup/', signupUser, name='signup' ),
    path('login/', loginUser, name='login'),
    path('logout/',logoutUser, name='logout'),
    path('comment/<int:postId>/', addComment, name='comment')
]