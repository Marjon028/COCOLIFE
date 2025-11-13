from django.contrib import admin
from .models import Product, ProductInfo, ProductInfoImage , PolicyOwner, PolicyOwnerData, TypeOfNeed,PolicyOwnerPdfFile

@admin.register(ProductInfoImage)
class ProductInfoImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'alt_text', 'visibility', 'created_at')
    model = ProductInfoImage
    search_fields = ('id',)


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user', 'created_at', 'updated_at')
    search_fields = ('product_name',)

@admin.register(TypeOfNeed)
class TypeOfNeedInfoAdmin(admin.ModelAdmin):
    list_display= ('name','description','created_at','updated_at','active')
    search_fields= ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at', 'updated_at')
    search_fields = ('name',)



@admin.register(PolicyOwner)
class PolicyOwnerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(PolicyOwnerPdfFile)
class PolicyOwnerPdfFileAdmin(admin.ModelAdmin):
    list_display=('product','mapping','pdf_file','user','created_at','updated_at')
    search_fields=('product',)

@admin.register(PolicyOwnerData)
class PolicyOwnerDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name')
    search_fields = ('title', 'first_name', 'last_name')





