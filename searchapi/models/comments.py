from django.db import models
from .user import User
from datetime import datetime

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	youtube_vid_id = models.CharField(null=True, max_length=255)
	text = models.TextField()
	date = models.DateTimeField(default=datetime.now, blank=True)
