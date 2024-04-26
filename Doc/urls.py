from django.urls import path
from Doc.views import *

urlpatterns = [
    path('upload/', DocUpload.as_view()),
    path('download/', DocDownload.as_view()),
    path('list/', DocList.as_view()),
    path('delete/', DocDelete.as_view()),
]
