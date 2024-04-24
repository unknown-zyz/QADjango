from django.urls import path
from Chat.views import *

urlpatterns = [
    path('', ChatCreateAPIView.as_view()),
    path('list/<int:pk>', ChatListAPIView.as_view()),
    path('<int:pk>/', ChatRetrieveUpdateDestroyAPIView.as_view()),
    path('export/<int:pk>/', ExportRepairOrder.as_view()),
]
