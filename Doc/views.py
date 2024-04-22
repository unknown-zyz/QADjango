from rest_framework import generics, status
from rest_framework.response import Response
from .models import Doc
from .serializers import DocSerializer
from datetime import date
from django.http import HttpResponse
from DocSet.models import DocSet


class DocUpload(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        remark = request.data.get('remark')
        docSet_id = request.data.get('docSet')
        if Doc.objects.filter(name=uploaded_file.name, docSet_id=docSet_id).exists():
            return Response({'error': 'File name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        elif DocSet.objects.filter(id=docSet_id, is_active=True).first() is None:
            return Response({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        Doc.objects.create(file=uploaded_file, name=uploaded_file.name, file_size=uploaded_file.size,
                           date=date.today(), remark=remark, docSet_id=docSet_id)
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


class DocList(generics.ListAPIView):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer

    def get(self, request, *args, **kwargs):
        docSet_id = self.kwargs.get('pk')
        if docSet_id is not None:
            if DocSet.objects.filter(id=docSet_id, is_active=True).first() is None:
                return Response({'error': 'DocSet does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = Doc.objects.filter(docSet_id=docSet_id, is_active=True).all()
        else:
            queryset = Doc.objects.filter(is_active=True).all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DocDelete(generics.DestroyAPIView):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer
