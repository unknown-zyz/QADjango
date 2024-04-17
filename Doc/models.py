from django.db import models
from DocSet.models import DocSet
import os


def doc_file_path(instance, filename):
    doc_set = instance.docSet
    return os.path.join('doc', str(doc_set.name), filename)


class Doc(models.Model):
    file = models.FileField(upload_to=doc_file_path)
    name = models.CharField(max_length=100)
    # status = models.CharField(max_length=50)
    file_size = models.FloatField()
    date = models.DateField()
    remark = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    docSet = models.ForeignKey(DocSet, on_delete=models.DO_NOTHING, related_name='docs')

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
