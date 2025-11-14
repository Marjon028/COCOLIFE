from .models import Product, ProductInfo, ProductInfoImage, PolicyOwner, default_policy_owner_data, default_address , PolicyOwnerData, TypeOfNeed, PolicyOwnerPdfFile
from rest_framework import serializers
from django.contrib.auth.models import User




class ProductInfoImageSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    #created_at = serializers.DateTimeField(allow_null=True, required=False, default=None)
    class Meta:
        model = ProductInfoImage
        fields = '__all__'
          
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']

class ProductInfoSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    product_images = ProductInfoImageSerializer(many=True,read_only=True)
    images_count = serializers.SerializerMethodField()
 

    class Meta:
        model = ProductInfo
        fields = [
            'id',
            'product',
            'product_name',
            'text1_extra',
            'text2_extra',
            'text3_extra',
            'text4_extra',
            'json_text_properties',
            'category',
            'type_of_need',
            'minimum_coverage_amount',
            'maximum_coverage_amount',
            'product_description',
            'benefits',
            'packages',
            'terms_and_conditions',
            'product_images',
            'images_count',
            'created_at',
            'updated_at',
            
        ]
    def get_images_count(self,obj):
        return obj.product_images.count()
        
   

class TypeOfNeedSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = TypeOfNeed
        fields = '__all__'



class PolicyOwnerPdfFileSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = PolicyOwnerPdfFile
        fields = '__all__'

class PolicyOwnerSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PolicyOwner
        fields = '__all__'
    
    '''def to_representation(self,instance):
        rep = super().to_representation(instance)
        for x,y in rep.items():
            print(x)
            rep[x] = instance.title['category']
        return rep'''
    def get_initial(self):
        """
        Kapag binuksan mo sa DRF browsable API (Raw Data),
        ito ang maglalabas ng default JSON structure.
        """
        initial = super().get_initial()

        default_json = {
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
        }

        # I-merge defaults sa initial data
        for key, value in default_json.items():
            if key not in initial or initial[key] in [None, ""]:
                initial[key] = value

        return initial


class PolicyOwnerDataSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    #user = UserSerializer(read_only=True)
    title_name = serializers.CharField(source='title.name', read_only=True)
    class Meta:
        model = PolicyOwnerData
        fields = ['id','product_name', 'title', 'title_name', 'first_name', 'middle_name', 'last_name', 'suffix',
                  'birthdate', 'birthplace', 'civil_status', 'gender', 'nationality', 'telephone_number',
                  'mobile_number', 'email_address', 'tin_number', 'sss_gsis_number', 'occupation', 'nature_of_business',
                  'specific_source_of_income', 'permanent_address', 'present_address', 'office_address',
                  'politically_exposed_person', 'are_you_sure_exposed_person', 'text1_extra', 'text2_extra',
                  'text3_extra', 'text4_extra']



class ProductSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    policy_owner_pdf_file = PolicyOwnerPdfFileSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id','name','type_of_need',
                  'description','created_at','updated_at','status','policy_owner_pdf_file']