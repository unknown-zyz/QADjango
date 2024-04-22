from django.http import JsonResponse
from rest_framework import generics

from .models import Chat
from DocSet.models import DocSet
from .serializers import ChatSerializer
from rest_framework import status


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
        Chat.objects.create(name=name, docSet_id=docSet_id)
        return JsonResponse({'success': 'Create success'}, status=status.HTTP_201_CREATED)


class ChatRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, **kwargs):
        chat = Chat.objects.get(pk=kwargs['pk'])
        return JsonResponse({'ChatHistory': chat.getHistory()})

    def post(self, request, **kwargs):
        chat = Chat.objects.get(pk=kwargs['pk'])
        user_content = {
            "role": "user",
            "content": request.data['content']
        }
        chat.updateHistory(user_content)
        # todo:post llm
        ai_content = {
            "role": "ai",
            "content": "xxx"
        }
        chat.updateHistory(ai_content)
        return JsonResponse({'success': 'chat success'}, status=status.HTTP_200_OK)
