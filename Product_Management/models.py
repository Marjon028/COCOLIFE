from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import fitz





def default_policy_owner_data():
    return {
        "name": "",
        "required": True,
        "field_type": ["text", "number", "date", "email", "dropdown", "radio", "checkbox", "textarea"],
        "key": "",
        "category": ""
    }

def default_address():
    return {
        "name": "",
        "required": True,
        "field_type": ["text", "number", "date", "email", "dropdown", "radio", "checkbox", "textarea"],
        "value": "",
        "category": "",
        "street": "",
        "city": "",
        "state": "",
        "zip_code": "",
        "country": "Philippines"
    }


class TypeOfNeed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type_of_need= models.ForeignKey(TypeOfNeed,related_name='type_of_needs',on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ('active', 'Active'),
            ('draft', 'Draft'),
            ('archived', 'Archived'),
        ],
        default='active'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductInfo(models.Model):
    product= models.OneToOneField(Product,on_delete=models.CASCADE)
    product_name = models.JSONField(max_length=255)
    text1_extra = models.JSONField(blank=True, null=True)
    text2_extra = models.JSONField(blank=True, null=True)
    text3_extra = models.JSONField(blank=True, null=True)
    text4_extra = models.JSONField(blank=True, null=True)
    json_text_properties = models.JSONField(blank=True, null=True)
    category = models.JSONField(blank=True, null=True)
    type_of_need = models.JSONField(blank=True, null=True)
    minimum_coverage_amount = models.JSONField(blank=True, null=True)
    maximum_coverage_amount = models.JSONField(blank=True, null=True)
    
    product_description = models.JSONField(blank=True, null=True)
    benefits = models.JSONField(blank=True, null=True)
    packages = models.JSONField(blank=True, null=True)
    terms_and_conditions = models.FileField(upload_to='terms_and_conditions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = "Product Info"
        verbose_name_plural = "Product Infos"


class ProductInfoImage(models.Model):
    product_info = models.ForeignKey(
        ProductInfo,
        related_name='product_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='product_info_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.alt_text or f"Image for {self.product_info.product_name}"
    
    class Meta:
        verbose_name = "Product Info Image"
        verbose_name_plural = "Product Info Images"


class PolicyOwner(models.Model):
    
    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.JSONField(default=default_policy_owner_data)
    first_name = models.JSONField(default=default_policy_owner_data)
    middle_name = models.JSONField(default=default_policy_owner_data)
    last_name = models.JSONField(default=default_policy_owner_data)
    suffix = models.JSONField(default=default_policy_owner_data)
    birthdate = models.JSONField(default=default_policy_owner_data)
    birthplace = models.JSONField(default=default_policy_owner_data)
    civil_status = models.JSONField(default=default_policy_owner_data)
    gender = models.JSONField(default=default_policy_owner_data)
    nationality = models.JSONField(default=default_policy_owner_data)
    telephone_number = models.JSONField(default=default_policy_owner_data)
    mobile_number = models.JSONField(default=default_policy_owner_data)
    email_address = models.JSONField(default=default_policy_owner_data)
    tin_number = models.JSONField(default=default_policy_owner_data)
    sss_gsis_number = models.JSONField(default=default_policy_owner_data)
    occupation = models.JSONField(default=default_policy_owner_data)
    nature_of_business = models.JSONField(default=default_policy_owner_data)
    specific_source_of_income = models.JSONField(default=default_policy_owner_data)
    permanent_address = models.JSONField(default=default_address)  
    present_address = models.JSONField(default=default_address)
    office_address = models.JSONField(default=default_address)
    politically_exposed_person = models.JSONField(default=default_policy_owner_data)
    are_you_sure_exposed_person = models.JSONField(default=default_policy_owner_data)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    text1_extra = models.JSONField(blank=True, null=True)
    text2_extra = models.JSONField(blank=True, null=True)
    text3_extra = models.JSONField(blank=True, null=True)
    text4_extra = models.JSONField(blank=True, null=True)
    

    def __str__(self):
        return f"PolicyOwner for {self.product.name}"
    class Meta:
        verbose_name = "Policy Owner"
        verbose_name_plural = "Policy Owners"


import fitz  # PyMuPDF
from django.db import models
from django.contrib.auth.models import User

class PolicyOwnerPdfFile(models.Model):
    product = models.OneToOneField(
        'Product', related_name='policy_owner_pdf_file', on_delete=models.CASCADE
    )
    mapping = models.JSONField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def extract_form_fields(self):
        """Extract text field names and values from a fillable PDF."""
        field_data = {}
        with fitz.open(self.pdf_file.path) as pdf:
            for page in pdf:
                widgets = page.widgets() or []
                for w in widgets:
                    if w.field_name:
                        field_data[w.field_name] = w.field_value or ""
        return field_data

    def save(self, *args, **kwargs):
        """Override save() to auto-extract form fields."""
        super().save(*args, **kwargs)
        try:
            self.mapping = self.extract_form_fields()
            super().save(update_fields=['mapping'])
        except Exception as e:
            print(f"[PDF FIELD ERROR] {e}")



class PolicyOwnerData(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.ForeignKey(PolicyOwner, related_name='policy_owner_data', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    suffix = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.CharField(max_length=255, null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    civil_status = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    telephone_number = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    tin_number = models.CharField(max_length=255, null=True, blank=True)
    sss_gsis_number = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    nature_of_business = models.CharField(max_length=255, null=True, blank=True)
    specific_source_of_income = models.CharField(max_length=255, null=True, blank=True)
    permanent_address = models.CharField(max_length=255, null=True, blank=True) 
    present_address = models.CharField(max_length=255, null=True, blank=True)
    office_address = models.CharField(max_length=255, null=True, blank=True)
    politically_exposed_person = models.CharField(max_length=255, null=True, blank=True)
    are_you_sure_exposed_person = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    text1_extra = models.CharField(max_length=255, null=True, blank=True)
    text2_extra = models.CharField(max_length=255, null=True, blank=True)
    text3_extra = models.CharField(max_length=255, null=True, blank=True)
    text4_extra = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Policy Owner Data"
        verbose_name_plural = "Policy Owner Data"

    def __str__(self):
        return f"PolicyOwnerData for {self.title}"


    
    

