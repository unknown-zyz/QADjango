from django.db import models
from User.models import User


class DocSet(models.Model):
    name = models.CharField(max_length=100)
