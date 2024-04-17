from django.urls import path
from Doc import views

urlpatterns = [
    path('upload', views.DocUpload.as_view()),
    path('download/<int:pk>', views.DocDownload.as_view()),
]
