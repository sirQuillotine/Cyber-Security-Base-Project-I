from django.db import models

from django.contrib.auth.models import User

class Account(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	iban = models.TextField(unique=True)
	balance = models.IntegerField(default=0)