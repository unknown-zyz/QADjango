from django.urls import path
from Doc.views import *

urlpatterns = [
    path('upload/', DocUpload.as_view()),
    path('download/<int:pk>/', DocDownload.as_view()),
    path('list/', DocList.as_view()),
    path('list/<int:pk>/', DocList.as_view()),
    path('<int:pk>/', DocDelete.as_view()),
]
