import requests
from django_q.tasks import async_task
from rest_framework import generics, status
from rest_framework.response import Response
from .models import DocSet
from .serializers import DocSetSerializer
from django.http import JsonResponse
from djangoProject.settings import LLM_URL


# def docset_name_cat(id, type):
#     docset = DocSet.objects.get(id=id)
#     return docset.name + '_' + type


def get_docset_id(id, type):
    docset = DocSet.objects.get(id=id)
    if type=="AMM":
        return docset.amm_id
    else:
        return docset.fim_id


def docset_create_task(docset):
    url = f'{LLM_URL}/docsets/'
    js = {"name": docset.name+"_AMM"}
    res = requests.post(url, json=js)
    docset.amm_id = res.json()['id']
    js = {"name": docset.name+"_FIM"}
    res = requests.post(url, json=js)
    docset.fim_id = res.json()['id']
    docset.save()
    print(res)


def docset_delete_task(docset_id):
    docset = DocSet.objects.get(id=id)
    url = f'{LLM_URL}/docsets/{docset.amm_id}'
    res = requests.delete(url)
    url = f'{LLM_URL}/docsets/{docset.fim_id}'
    res = requests.delete(url)
    print(res)


class DocSetListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        if not name:
            return JsonResponse({'error': 'DocSet name is required'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if DocSet.objects.filter(name=name).exists():
            return JsonResponse({'error': 'DocSet name already exists'}, status=status.HTTP_409_CONFLICT)
        docset = DocSet.objects.create(name=name)
        async_task(docset_create_task, docset)
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
        async_task(docset_delete_task, docset_id)
        return Response({'success': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)
