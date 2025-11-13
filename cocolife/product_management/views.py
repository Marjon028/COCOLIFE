from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.



from rest_framework import viewsets,status
from .models import Policy_Owner, Policy_Owner_Fields, Policy_Owner_Values
from .serializers import PolicyOwnerSerializer, PolicyOwnerFieldSerializer,PolicyOwnerValueSerializer, PolicyOwnerFieldOnlySerializer, PolicyOwnerTableFormatSerializer


class PolicyOwnerTableFormatViewSet(viewsets.ModelViewSet):
    queryset = Policy_Owner.objects.all().prefetch_related(
        'fields__values',  # assuming related_name="values" sa model mo
        'fields'
    )
    serializer_class = PolicyOwnerTableFormatSerializer


class PolicyOwnerViewSet(viewsets.ModelViewSet):
    queryset = Policy_Owner.objects.all().prefetch_related(
        'fields__values',  # assuming related_name="values" sa model mo
        'fields'
    )
  
    #queryset = Policy_Owner.objects.all()
    serializer_class = PolicyOwnerSerializer

class PolicyOwnerFieldViewSet(viewsets.ModelViewSet):
    queryset = Policy_Owner_Fields.objects.all()
    serializer_class = PolicyOwnerFieldSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Custom endpoint: POST /policy-fields/bulk_create/
        Tumanggap ng listahan ng fields para sabay-sabay i-save.
        """
        data = request.data  # Expecting a list of dicts
        if not isinstance(data, list):
            return Response({"error": "Data should be a list of fields"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        Policy_Owner_Fields.objects.bulk_create(
            [Policy_Owner_Fields(**item) for item in serializer.validated_data]
        )
        return Response({"message": f"{len(data)} fields created successfully!"}, status=status.HTTP_201_CREATED)

class PolicyOwnerFieldOnlyViewSet(viewsets.ModelViewSet):
    queryset = Policy_Owner_Fields.objects.all()
    serializer_class = PolicyOwnerFieldOnlySerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Policy_Owner_Values
from .serializers import PolicyOwnerValueSerializer
from django.db.models import Max

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Max
from .models import Policy_Owner_Values
from .serializers import PolicyOwnerValueSerializer


class PolicyOwnerValueViewSet(viewsets.ModelViewSet):
    queryset = Policy_Owner_Values.objects.all()
    serializer_class = PolicyOwnerValueSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        POST /policy-values/bulk_create/
        Tumanggap ng listahan ng values (isang row ng fields) 
        at sabay-sabay i-save (bulk create) na may shared row_number.
        """
        data = request.data  # expecting a list of dicts
        if not isinstance(data, list):
            return Response({"error": "Data should be a list of objects"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not validated_data:
            return Response({"error": "Empty data"}, status=status.HTTP_400_BAD_REQUEST)

        # assume all items in this batch belong to the same policy_owner
        policy_owner = validated_data[0]["policy_owner"]

        # get current last row_number for this policy_owner
        last_row = (
            Policy_Owner_Values.objects.filter(policy_owner=policy_owner)
            .aggregate(last=Max("row_number"))
            .get("last")
        )
        next_row_number = (last_row or 0) + 1

        # assign same row_number to all items in this batch
        new_objects = [
            Policy_Owner_Values(
                policy_owner=item["policy_owner"],
                field=item["field"],
                value=item["value"],
                row_number=next_row_number,
            )
            for item in validated_data
        ]

        Policy_Owner_Values.objects.bulk_create(new_objects)

        return Response(
            {
                "message": f"{len(new_objects)} values created for row {next_row_number} successfully!"
            },
            status=status.HTTP_201_CREATED,
        )
