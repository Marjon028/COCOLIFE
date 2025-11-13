from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')  # images will be stored in media/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Document(models.Model):
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/')
# Create your models here.
