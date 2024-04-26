from django.http import JsonResponse
from rest_framework import generics, status

from .models import Chat
from DocSet.models import DocSet
from .serializers import ChatSerializer
import requests
from rest_framework.views import APIView
from django_q.tasks import async_task


def chat_create_task(name, docset_id):
    url = f'http://172.16.26.4:8081/chats/'
    js = {"name": name, "document_set_id": docset_id}
    res = requests.post(url, json=js)
    print(res)


class ChatCreateAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        docSet_id = request.data.get('docSet')
        if Chat.objects.filter(name=name, docSet_id=docSet_id).exists():
            return JsonResponse({'error': 'Chat name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        elif DocSet.objects.filter(id=docSet_id, is_active=True).first() is None:
            return JsonResponse({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        chat = Chat.objects.create(name=name, docSet_id=docSet_id)
        async_task(chat_create_task, name, docSet_id)
        return JsonResponse({'success': 'Create success', 'chat_id': chat.id}, status=status.HTTP_201_CREATED)


class ChatListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        docSet_id = self.request.query_params.get('docset')
        if DocSet.objects.filter(id=docSet_id, is_active=True).first() is None:
            return JsonResponse({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        queryset = Chat.objects.filter(docSet_id=docSet_id).all()
        serializer = ChatSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class ChatRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, **kwargs):
        chat = Chat.objects.get(pk=self.request.query_params.get('chat'))
        return JsonResponse({'ChatHistory': chat.getHistory()}, status=status.HTTP_200_OK)


class ChatChatAPIView(APIView):
    def post(self, request, **kwargs):
        chat_id = self.request.query_params.get('chat')
        content = request.data['content']
        chat = Chat.objects.get(pk=chat_id)
        user_content = {
            "isLlm": False,
            "content": content
        }
        chat.updateHistory(user_content)
        url = f'http://172.16.26.4:8081/chats/{chat_id}/'
        ret = requests.post(url, json={"content": content}).json()['message']['content']
        ai_content = {
            "isLlm": True,
            "content": ret
        }
        chat.updateHistory(ai_content)
        return JsonResponse({'content': ret}, status=status.HTTP_200_OK)


class ChatDestroyAPIView(generics.DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def destroy(self, request, *args, **kwargs):
        chat_id = self.request.query_params.get('chat')
        try:
            instance = self.get_queryset().get(pk=chat_id)
        except Chat.DoesNotExist:
            return JsonResponse({'error': 'Chat does not exist'}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return JsonResponse({'success': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)


class ExportRepairOrder(APIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, **kwargs):
        chat_id = self.request.query_params.get('chat')
        chat = Chat.objects.get(pk=chat_id)
        user_content = {
            "isLlm": False,
            "content": "生成维修记录单"
        }
        chat.updateHistory(user_content)
        url = f'http://172.16.26.4:8081/chats/{chat_id}/'
        ret = requests.post(url, json={"content": "生成维修记录单"}).json()['message']['content']
        ai_content = {
            "isLlm": True,
            "content": ret
        }
        chat.updateHistory(ai_content)
        return JsonResponse({'ChatHistory': chat.getHistory()}, status=status.HTTP_200_OK)
