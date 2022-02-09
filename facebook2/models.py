from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Story(models.Model):
	content = models.TextField()
	tags = models.CharField(max_length=100)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)
