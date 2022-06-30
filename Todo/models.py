from django.db import models
from django.conf import settings

# Create your models here.

class Todo(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.name