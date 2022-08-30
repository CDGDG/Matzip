from tkinter import CASCADE
from django.db import models

from django.contrib.auth.models import User

from matzip.models import Restaurant

class Comment(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_column='user')
    text = models.TextField(null=False, default="", db_column='text')
    rating = models.IntegerField(null=False, db_column='rating')
    datetime = models.DateTimeField(null=False, auto_now_add=True, db_column='datetime')
    matzip = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False, db_column="matzip")

    class Meta:
        db_table = 'mz_comment'

    def __str__(self):
        return f"{self.user.username} : {self.text}"


class CommentImage(models.Model):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, db_column="comment", related_name="coim")
    image = models.FileField(null=False, upload_to="comment_image/", db_column="image")

    class Meta:
        db_table = "mz_commentimage"
    
