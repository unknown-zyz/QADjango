from rest_framework import generics, status
from .models import DocSet
from .serializers import DocSetSerializer
from django.http import JsonResponse


class DocSetListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer

    def get_queryset(self):
        return DocSet.objects.filter(is_active=True).all()

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        if DocSet.objects.filter(name=name).exists():
            return JsonResponse({'error': 'DocSet name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        DocSet.objects.create(name=name)
        return JsonResponse({'success': 'Create success'}, status=status.HTTP_201_CREATED)


class DocSetDestroyAPIView(generics.DestroyAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer
