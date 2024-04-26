from django.urls import path
from DocSet.views import *

urlpatterns = [
    path('', DocSetListCreateAPIView.as_view()),
    path('delete/', DocSetDestroyAPIView.as_view()),
]
