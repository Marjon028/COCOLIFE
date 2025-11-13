from .views import ProductViewSet, ProductInfoViewSet, ProductInfoImageViewSet, PolicyOwnerViewSet, PolicyOwnerDataViewSet, TypeOfNeedViewSet, PolicyOwnerPdfFileViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
router = DefaultRouter()

router.register(r'product-info', ProductInfoViewSet)
router.register(r'product-info-images', ProductInfoImageViewSet)

router.register(r'type-of-need',TypeOfNeedViewSet)
router.register(r'products', ProductViewSet)
router.register(r'policy-owner-pdf-file',PolicyOwnerPdfFileViewSet)
router.register(r'policy-owners', PolicyOwnerViewSet)
router.register(r'policy-owner-data', PolicyOwnerDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]