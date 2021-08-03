from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="original_poster")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id" : self.id,
            "user" : self.user.username,
            "text" : self.text,
            "timestamp" : self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
        }
    def __str__(self):
        return f'{self.text[:10]} by {self.user}'

class Follow(models.Model):
    following = models.ForeignKey("User", on_delete= models.CASCADE, related_name="following")
    follower = models.ForeignKey("User", on_delete= models.CASCADE, related_name="follower")
    number=models.IntegerField(default=0,blank=True)
    def serialize(self):
        return {
            "following" : self.following.username,
            "follower" : self.follower.username
        }
    def __str__(self):
        return f'{self.following} is followed by {self.follower}'
        

class Like(models.Model):
    likedby = models.ForeignKey("User", on_delete= models.CASCADE, related_name="liker")
    post = models.ForeignKey("Post", on_delete= models.CASCADE, related_name="postliked")
    def serialize(self):
        return {
            "likedby" : self.likedby.username,
            "post" : self.post.id
        }
    def __str__(self):
        return f'{self.likedby} likes post #{self.post.id}'
    