import json

import requests
from django_q.tasks import async_task
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Doc
from .serializers import DocSerializer
from datetime import date
from django.http import HttpResponse


def upload_task(docset_id, file):
    if Doc.objects.filter(name=file.name, docSet_id=docset_id):
        doc = Doc.objects.get(name=file.name, docSet_id=docset_id)
        url = f'http://172.16.26.4:8000/docsets/{docset_id}/docs'
        headers = {'accept': 'application/json'}
        files = {'file': (file.name, file.file, 'application/pdf')}
        res = requests.post(url, headers=headers, files=files)
        if res.status_code == 200:
            doc.upload_status = "Success"
        else:
            doc.upload_status = "Failed"
        doc.save()


class DocUpload(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        remark = request.data.get('remark')
        docSet_id = request.data.get('docSet')
        if Doc.objects.filter(name=uploaded_file.name, docSet_id=docSet_id).exists():
            return Response({'error': 'File name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        Doc.objects.create(file=uploaded_file, name=uploaded_file.name, file_size=uploaded_file.size,
                           date=date.today(), remark=remark, docSet_id=docSet_id)
        async_task(upload_task, docSet_id, uploaded_file)
        return Response({'success': 'Upload success'}, status=status.HTTP_201_CREATED)


class DocDownload(generics.RetrieveAPIView):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="' + instance.name + '"'
            return response

# 实现返回doc列表

