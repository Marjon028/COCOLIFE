from rest_framework import serializers
from .models import Photo
from .models import Document
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'image', 'uploaded_at']



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'pdf_file']

    def get_file_url(self, obj):
        request = self.context.get('request')  # kunin ang request
        if request:
            return request.build_absolute_uri(obj.file.url)  # buo na ang URL
        return obj.file.url
