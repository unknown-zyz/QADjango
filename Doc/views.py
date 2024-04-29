import requests
from django_q.tasks import async_task
from rest_framework import generics, status
from django.http import JsonResponse
from .models import Doc
from .serializers import DocSerializer
from datetime import date
from django.http import HttpResponse
from DocSet.models import DocSet


def doc_upload_task(docset_id, file_name, file_content):
    if Doc.objects.filter(name=file_name, docSet_id=docset_id):
        doc = Doc.objects.get(name=file_name, docSet_id=docset_id)
        url = f'http://172.16.26.4:8081/docsets/{docset_id}/docs'
        headers = {'accept': 'application/json'}
        files = [('files', (file_name, file_content, 'application/pdf'))]
        res = requests.post(url, headers=headers, files=files)
        print(res)
        if res.status_code == 200:
            doc.upload_status = "Success"
        else:
            doc.upload_status = "Failed"
        doc.save()


def doc_delete_task(doc_id):
    url = f'http://172.16.26.4:8081/docs/{doc_id}'
    res = requests.delete(url)
    print(res)


class DocUpload(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        remark = request.data.get('remark')
        docSet_id = request.data.get('docSet')
        if Doc.objects.filter(name=uploaded_file.name, docSet_id=docSet_id).exists():
            return JsonResponse({'error': 'File name already exists'}, status=status.HTTP_409_CONFLICT)
        elif DocSet.objects.filter(id=docSet_id).first() is None:
            return JsonResponse({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        Doc.objects.create(file=uploaded_file, name=uploaded_file.name,
                           file_size=round(uploaded_file.size / (1024 * 1024), 2),
                           date=date.today(), remark=remark, docSet_id=docSet_id)
        uploaded_file.seek(0)
        file_content = uploaded_file.read()
        async_task(doc_upload_task, docSet_id, uploaded_file.name, file_content)
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
        if DocSet.objects.filter(id=docSet_id).first() is None:
            return JsonResponse({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        queryset = Doc.objects.filter(docSet_id=docSet_id).all()
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
        async_task(doc_delete_task, doc_id)
        return JsonResponse({'success': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)
