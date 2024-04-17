from rest_framework import generics, status
from rest_framework.response import Response
from .models import Doc
from .serializers import DocSerializer
from datetime import date
from django.http import HttpResponse


class DocUpload(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = self.request.FILES.get('file')
        remark = self.request.data.get('remark')
        if Doc.objects.filter(name=uploaded_file.name).exists():
            return Response({'error': 'File name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        Doc.objects.create(file=uploaded_file, name=uploaded_file.name, file_size=uploaded_file.size,
                           date=date.today(), remark=remark)
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
