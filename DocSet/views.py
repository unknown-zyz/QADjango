from rest_framework import generics
from .models import DocSet
from .serializers import DocSetSerializer


class DocSetListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer


class DocSetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer
