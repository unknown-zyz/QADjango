from django.urls import path
from Chat.views import *

urlpatterns = [
    path('', ChatListCreateAPIView.as_view()),
    path('<int:pk>/', ChatRetrieveUpdateDestroyAPIView.as_view()),
    path('export/<int:pk>/', ExportRepairOrder.as_view()),
]
