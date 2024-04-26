import requests
from django_q.tasks import async_task
from rest_framework import generics, status
from rest_framework.response import Response
from .models import DocSet
from .serializers import DocSetSerializer
from django.http import JsonResponse


def docset_create_task(name):
    url = f'http://172.16.26.4:8081/docsets/'
    js = {"name": name}
    res = requests.post(url, json=js)
    print(res)


class DocSetListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer

    def get_queryset(self):
        return DocSet.objects.filter(is_active=True).all()

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        if not name:
            return JsonResponse({'error': 'DocSet name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if DocSet.objects.filter(name=name).exists():
            return JsonResponse({'error': 'DocSet name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        DocSet.objects.create(name=name)
        async_task(docset_create_task, name)
        return JsonResponse({'success': 'Create success'}, status=status.HTTP_201_CREATED)


class DocSetDestroyAPIView(generics.DestroyAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer

    def destroy(self, request, *args, **kwargs):
        docset_id = self.request.query_params.get('docset')
        try:
            instance = self.get_queryset().get(pk=docset_id)
        except DocSet.DoesNotExist:
            return Response({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response({'success': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)

