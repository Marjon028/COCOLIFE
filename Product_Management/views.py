from django.shortcuts import render
from .models import Product, ProductInfo, ProductInfoImage , PolicyOwner , default_address, default_policy_owner_data , PolicyOwnerData, TypeOfNeed, PolicyOwnerPdfFile
from .serializers import ProductSerializer, ProductInfoSerializer, ProductInfoImageSerializer, PolicyOwnerSerializer , PolicyOwnerDataSerializer, TypeOfNeedSerializer, PolicyOwnerPdfFileSerializer
# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''


class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    #permission_classes = [IsAuthenticated]

    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''

class ProductInfoImageViewSet(viewsets.ModelViewSet):
    queryset = ProductInfoImage.objects.all()
    serializer_class = ProductInfoImageSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''

class PolicyOwnerPdfFileViewSet(viewsets.ModelViewSet):
    queryset = PolicyOwnerPdfFile.objects.all()
    serializer_class= PolicyOwnerPdfFileSerializer

    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''

class PolicyOwnerViewSet(viewsets.ModelViewSet):
    queryset = PolicyOwner.objects.all()
    serializer_class = PolicyOwnerSerializer

    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''

    filter_backends= [filters.SearchFilter]
    search_fields = ['product__name','product__id']

    def list(self, request, *args, **kwargs):
        """Kapag wala pang laman sa DB, ipakita default JSON structure."""
        queryset = self.get_queryset()
        if not queryset.exists():
            default_data = {
                "product_name": "",
                "title": default_policy_owner_data(),
                "first_name": default_policy_owner_data(),
                "middle_name": default_policy_owner_data(),
                "last_name": default_policy_owner_data(),
                "suffix": default_policy_owner_data(),
                "birthdate": default_policy_owner_data(),
                "birthplace": default_policy_owner_data(),
                "civil_status": default_policy_owner_data(),
                "gender": default_policy_owner_data(),
                "nationality": default_policy_owner_data(),
                "telephone_number": default_policy_owner_data(),
                "mobile_number": default_policy_owner_data(),
                "email_address": default_policy_owner_data(),
                "tin_number": default_policy_owner_data(),
                "sss_gsis_number": default_policy_owner_data(),
                "occupation": default_policy_owner_data(),
                "nature_of_business": default_policy_owner_data(),
                "specific_source_of_income": default_policy_owner_data(),
                "permanent_address": default_address(),
                "present_address": default_address(),
                "office_address": default_address(),
                "politically_exposed_person": default_policy_owner_data(),
                "are_you_sure_exposed_person": default_policy_owner_data(),
                "text1_extra": None,
                "text2_extra": None,
                "text3_extra": None,
                "text4_extra": None,
               # "user": None,
            }
            return Response(default_data)
        # Default behavior kung may laman na
        return super().list(request, *args, **kwargs)



class PolicyOwnerDataViewSet(viewsets.ModelViewSet):
    queryset = PolicyOwnerData.objects.all()
    serializer_class = PolicyOwnerDataSerializer
    
    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''

class TypeOfNeedViewSet(viewsets.ModelViewSet):
    queryset = TypeOfNeed.objects.all()
    serializer_class = TypeOfNeedSerializer

    '''def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''