from django.db import models

class DocSet(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.docs.all().update(is_active=False)
        self.save()
