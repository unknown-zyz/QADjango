from django.urls import path
from Chat.views import *

urlpatterns = [
    path('', ChatCreateAPIView.as_view()),
    path('list/', ChatListAPIView.as_view()),
    path('history/', ChatRetrieveAPIView.as_view()),
    path('chat/', ChatChatAPIView.as_view()),
    path('delete/', ChatDestroyAPIView.as_view()),
    path('export/<int:pk>/', ExportRepairOrder.as_view()),
]
