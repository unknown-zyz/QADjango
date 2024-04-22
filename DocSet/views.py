from rest_framework import generics
from .models import DocSet
from .serializers import DocSetSerializer


class DocSetListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer

    def get_queryset(self):
        return DocSet.objects.filter(is_active=True).all()


class DocSetDestroyAPIView(generics.DestroyAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer
