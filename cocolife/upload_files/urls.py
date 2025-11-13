from django.urls import path
from .views import PhotoViewSet
from .views import DocumentUploadView
urlpatterns = [
    path('photos/', PhotoViewSet.as_view({'get': 'list', 'post': 'create'}), name='photo-list'),
    path('photos/<int:pk>/', PhotoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='photo-detail'),
    path('upload-pdf/', DocumentUploadView.as_view(), name='upload-pdf'),
    path('upload-pdf/<int:pk>/', DocumentUploadView.as_view(), name='upload-pdf-detail'),
    
]