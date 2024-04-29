from django.http import JsonResponse, FileResponse, HttpResponse
from rest_framework import generics, status

from .models import Chat
from DocSet.models import DocSet
from .serializers import ChatSerializer
import requests, json
from rest_framework.views import APIView
from django_q.tasks import async_task


def chat_create_task(name, docset_id):
    url = f'http://172.16.26.4:8081/chats/'
    js = {"name": name, "document_set_id": docset_id}
    res = requests.post(url, json=js)
    print(res)


def chat_delete_task(chat_id):
    url = f'http://172.16.26.4:8081/chats/{chat_id}'
    res = requests.delete(url)
    print(res)


class ChatCreateAPIView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        docSet_id = request.data.get('docSet')
        if Chat.objects.filter(name=name, docSet_id=docSet_id).exists():
            return JsonResponse({'error': 'Chat name already exists'}, status=status.HTTP_409_CONFLICT)
        elif DocSet.objects.filter(id=docSet_id).first() is None:
            return JsonResponse({'error': 'DocSet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        chat = Chat.objects.create(name=name, docSet_id=docSet_id)
        async_task(chat_create_task, name, docSet_id)
        return JsonResponse({'success': 'Create success', 'chat_id': chat.id}, status=status.HTTP_201_CREATED)


class ChatListAPIView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        docSet_id = self.request.query_params.get('docset')
        if DocSet.objects.filter(id=docSet_id).first() is None:
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
            "content": content,
            "ifshowSource": False,
            "sourceNum": 1,
            "sourceList": [
                {
                    "content": "文档5第555行",
                }
            ]
        }
        chat.updateHistory(user_content)
        url = f'http://172.16.26.4:8081/chats/{chat_id}/'
        response = requests.post(url, json={"content": content})
        if response.status_code != 200:
            data = "大模型服务异常，请稍后再试"
        else:
            data = response.json()['message']['content']
        ai_content = {
            "isLlm": True,
            "content": data,
            "ifshowSource": False,
            "sourceNum": 1,
            "sourceList": [
                {
                    "content": "文档5第555行",
                }
            ]
        }
        chat.updateHistory(ai_content)
        return JsonResponse(ai_content, status=status.HTTP_200_OK)


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
        async_task(chat_delete_task, chat_id)
        return JsonResponse({'success': 'Delete success'}, status=status.HTTP_204_NO_CONTENT)


class ExportRepairOrder(APIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, **kwargs):
        chat_id = self.request.query_params.get('chat')
        chat = Chat.objects.get(pk=chat_id)
        user_content = {
            "isLlm": False,
            "content": "生成维修记录单",
            "ifshowSource": False,
            "sourceNum": 1,
            "sourceList": [
                {
                    "content": "文档5第555行",
                }
            ]
        }
        chat.updateHistory(user_content)
        url = f'http://172.16.26.4:8081/chats/{chat_id}/'
        response = requests.post(url, json={"content": "生成维修记录单"})
        if response.status_code != 200:
            data = "大模型服务异常，请稍后再试"
        else:
            data = response.json()['message']['content']
        ai_content = {
            "isLlm": True,
            "content": data,
            "ifshowSource": False,
            "sourceNum": 1,
            "sourceList": [
                {
                    "content": "文档5第555行",
                }
            ]
        }
        chat.updateHistory(ai_content)
        with open('维修记录单.txt', 'w') as f:
            json.dump(ai_content, f)
        with open('维修记录单.txt', 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="维修记录单.txt"'
            return response
