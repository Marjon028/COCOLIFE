from rest_framework import serializers
from .models import Policy_Owner, Policy_Owner_Fields, Policy_Owner_Values

# Serializer para sa Values
class PolicyOwnerValueSerializer(serializers.ModelSerializer):
    policy_fields_name = serializers.ReadOnlyField(source='field.field_name')
    
    class Meta:
        model = Policy_Owner_Values

        fields = ['id', 'row_number', 'policy_fields_name', 'policy_owner', 'field', 'value', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        
        
        #return Policy_Owner_Values(**validated_data)
        return Policy_Owner_Values.objects.create(**validated_data)


# Serializer para sa Fields (kasama nested values)
class PolicyOwnerFieldSerializer(serializers.ModelSerializer):
    values = PolicyOwnerValueSerializer(many=True, required=False)
    policy_owner_name = serializers.ReadOnlyField(source='policy_owner.name')
    

    class Meta:
        model = Policy_Owner_Fields
        fields = ['id', 'policy_owner','policy_owner_name', 'field_name', 'field_type', 'field_type_list', 'is_required', 'values', 'created_at', 'updated_at']

# Serializer para sa Policy Owner (kasama nested fields at values)

from rest_framework import serializers
from collections import defaultdict

class PolicyOwnerTableFormatSerializer(serializers.ModelSerializer):
    grouped_rows = serializers.SerializerMethodField()

    class Meta:
        model = Policy_Owner  # Assuming ito ang model mo
        fields = ['id', 'grouped_rows']  # Id lang plus grouped rows

    def get_grouped_rows(self, obj):
        """
        I-group lahat ng Policy_Owner_Values ayon sa row.
        Bawat row ay dict ng field_name -> value
        """
        all_values = Policy_Owner_Values.objects.filter(policy_owner=obj).order_by('id')

        rows = []
        temp_row = {}

        # assuming bawat tao ay may parehong number ng fields (e.g., First_Name, Last_name)
        for value in all_values:
            temp_row[value.field.field_name] = value.value

            # kapag kumpleto na ang row (e.g., First_Name + Last_name), i-append sa rows
            # pwede i-check base sa field count ng model
            if len(temp_row) == Policy_Owner_Values.objects.filter(policy_owner=obj, field__isnull=False).values('field').distinct().count():
                rows.append(temp_row)
                temp_row = {}

        return rows

    class Meta:
        model = Policy_Owner
        fields = ['id', 'grouped_rows']
class PolicyOwnerSerializer(serializers.ModelSerializer):
    fields = PolicyOwnerFieldSerializer(many=True, required=False)
   

    class Meta:
        model = Policy_Owner
        fields = ['id', 'name', 'decription', 'label', 'fields', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Kunin ang fields data
        fields_data = validated_data.pop('fields', [])
        # Gumawa ng Policy Owner
        policy_owner = Policy_Owner.objects.create(**validated_data)

        # Gumawa ng bawat Field at Values kung meron
        for field_data in fields_data:
            values_data = field_data.pop('values', [])
            field = Policy_Owner_Fields.objects.create(policy_owner=policy_owner, **field_data)

            for value_data in values_data:
                Policy_Owner_Values.objects.create(policy_owner=policy_owner, field=field, **value_data)

        return policy_owner

    def update(self, instance, validated_data):
        # Update Policy Owner fields
        instance.name = validated_data.get('name', instance.name)
        instance.decription = validated_data.get('decription', instance.decription)
        instance.label = validated_data.get('label', instance.label)
        instance.save()

        # Optional: update nested fields at values
        # Dito pwedeng i-handle partial update sa nested fields kung kailangan

        return instance

class PolicyOwnerFieldOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy_Owner_Fields
        fields = ['id', 'policy_owner','field_name', 'field_type', 'field_type_list', 'is_required', 'created_at', 'updated_at']