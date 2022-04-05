from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


class Profile(models.Model):
    genderDef = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    avatar = CloudinaryField('image',)
    firstName = models.CharField(max_length=60, null=True)
    lastName = models.CharField(max_length=60, null=True)
    bio = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, choices=genderDef, null=True)


class Post(models.Model):
    image_url = CloudinaryField('image')
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='added_by')


class Like(models.Model):
    post_liked = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='liked_post')
    liked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_user')


class Comment(models.Model):
    comment = models.TextField()
    commented_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_commented')
    commentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commented_by')
