from .views import PolicyOwnerViewSet, PolicyOwnerFieldViewSet, PolicyOwnerValueViewSet, PolicyOwnerFieldOnlyViewSet ,PolicyOwnerTableFormatViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'policy-owners', PolicyOwnerViewSet, basename='policy-owner')
router.register(r'policy-fields', PolicyOwnerFieldViewSet, basename='policy-field')
router.register(r'policy-values', PolicyOwnerValueViewSet, basename='policy-value')
router.register(r'policy-fields-only', PolicyOwnerFieldOnlyViewSet, basename='policy-field-only')
router.register(r'policy-owners-table', PolicyOwnerTableFormatViewSet, basename='policy-owner-table')


urlpatterns = [
    path('', include(router.urls)),
]