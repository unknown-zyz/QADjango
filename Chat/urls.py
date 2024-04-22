from django.urls import path
from Chat.views import *

urlpatterns = [
    path('', ChatCreateAPIView.as_view()),
    path('<int:pk>/', ChatRetrieveUpdateDestroyAPIView.as_view()),
]
