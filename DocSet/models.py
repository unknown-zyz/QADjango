from django.db import models
from User.models import User


class DocSet(models.Model):
    name = models.CharField(max_length=100)
    amm_id = models.IntegerField(default=0)
    fim_id = models.IntegerField(default=0)