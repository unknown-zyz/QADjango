from django.db import models
from User.models import User


class DocSet(models.Model):
    name = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='docsets')
    is_active = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.docs.all().update(is_active=False)
        self.save()
