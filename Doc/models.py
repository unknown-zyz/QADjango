from django.db import models


# Create your models here.
class Doc(models.Model):
    file = models.FileField(upload_to='doc/')
    name = models.CharField(max_length=100)
    # status = models.CharField(max_length=50)
    file_size = models.FloatField()
    date = models.DateField()
    remark = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
