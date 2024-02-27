from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class Post(models.Model):
    poster=models.ForeignKey(User,on_delete=models.CASCADE,related_name="poster")
    post_content=models.TextField(default=None,verbose_name="New Post")
    date=models.DateTimeField(default=datetime.datetime.now())
    likes=models.ManyToManyField(User,blank=True,related_name="post")

    def __str__(self):
        return f"Post ID: {self.id}, By: {self.poster}"

class Profile(models.Model):
    person=models.ForeignKey(User,on_delete=models.CASCADE,related_name="person",default=None)
    following=models.ManyToManyField(User,blank=True,related_name="followers")
    follower=models.ManyToManyField(User,blank=True,related_name="following")

    def __str__(self):
        return f"{self.person}"

    def serialize(self):
        return {
            "id":self.id,
            "person":self.person,
            "following":[user.username for user in self.following.all()],
            "follower":[user.username for user in self.follower.all()]
        }