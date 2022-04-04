from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = CloudinaryField('image')
    bio = models.CharField(max_length=200)

class Post(models.Model):
    image_url = CloudinaryField('image')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.TextField()
    commented_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)