from django.urls import path
from DocSet.views import *

urlpatterns = [
    path('', DocSetListCreateAPIView.as_view()),
    path('<int:pk>/', DocSetDestroyAPIView.as_view()),
]
