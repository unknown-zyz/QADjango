import requests
from django_q.tasks import async_task
from rest_framework import generics, status
from django.http import JsonResponse
from .models import Doc
from .serializers import DocSerializer
from datetime import date
from django.http import HttpResponse
from DocSet.models import DocSet


def upload_task(docset_id, file):
    if Doc.objects.filter(name=file.name, docSet_id=docset_id):
        doc = Doc.objects.get(name=file.name, docSet_id=docset_id)
        url = f'http://172.16.26.4:8081/docsets/{docset_id}/docs'
        headers = {'accept': 'application/json'}
        file.seek(0)
        file_content = file.read()
        files = [('files', (file.name, file_content, 'application/pdf'))]
        res = requests.post(url, headers=headers, files=files)
        print(res)
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
            return JsonResponse({'error': 'File name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        elif DocSet.objects.filter(id=docSet_id, is_active=True).first() is None:
            return JsonResponse({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        Doc.objects.create(file=uploaded_file, name=uploaded_file.name, file_size=uploaded_file.size,
                           date=date.today(), remark=remark, docSet_id=docSet_id)
        async_task(upload_task, docSet_id, uploaded_file)
        return JsonResponse({'success': 'Upload success'}, status=status.HTTP_201_CREATED)


class DocDownload(generics.RetrieveAPIView):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer

    def get(self, request, *args, **kwargs):
        doc_id = self.request.query_params.get('doc')
        instance = Doc.objects.filter(id=doc_id).first()
        file_path = instance.file.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="' + instance.name + '"'
            return response


class DocList(generics.ListAPIView):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer

    def get(self, request, *args, **kwargs):
        docSet_id = self.request.query_params.get('docset')
        if DocSet.objects.filter(id=docSet_id, is_active=True).first() is None:
            return JsonResponse({'error': 'DocSet does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Doc.objects.filter(docSet_id=docSet_id, is_active=True).all()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class DocDelete(generics.DestroyAPIView):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer

    def destroy(self, request, *args, **kwargs):
        doc_id = self.request.query_params.get('doc')
        try:
            instance = self.get_queryset().get(pk=doc_id)
        except Doc.DoesNotExist:
            return JsonResponse({'error': 'Doc does not exist'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return JsonResponse({'success': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)
