from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer, DocumentSerializer

# Create your views here.
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


from . import forms
import PyPDF2  # or pdfminer.six
import mimetypes
from rest_framework.response import Response
from rest_framework.views import APIView
from PyPDF2 import PdfReader
from docx import Document
from .models import Document

from .serializers import DocumentSerializer


class DocumentUploadView(APIView):

    def get(self, request):
        documents = Document.objects.all()

        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)
        

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)

        if serializer.is_valid():
            doc = serializer.save()
            file_path = doc.pdf_file.path  # assuming the FileField is named 'pdf_file'
            content_type, _ = mimetypes.guess_type(file_path)

            fields = {}

            try:
                # === 🧾 PDF Handling ===
                if content_type == 'application/pdf':
                    with open(file_path, 'rb') as f:
                        pdf_reader = PdfReader(f)

                        # Check if PDF has AcroForm fields
                        if "/AcroForm" in pdf_reader.trailer["/Root"]:
                            fields = pdf_reader.get_form_text_fields() or {}
                            for x in fields.keys():
                                print("Extracted form fields:", x)
                        else:
                            # fallback: extract plain text
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text() or ""
                            fields = {"info": "No form fields found", "text": text.strip()}

                # === 📝 Word (.docx) Handling ===
                elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    docx_file = Document(file_path)
                    paragraphs = [p.text.strip() for p in docx_file.paragraphs if p.text.strip()]
                    fields = {
                        "info": "Word document content extracted",
                        "paragraphs": paragraphs,
                    }

                # === ❌ Unsupported file type ===
                else:
                    fields = {"error": f"Unsupported file type: {content_type}"}

            except Exception as e:
                fields = {"error": str(e)}

            return Response({
                "id": doc.id,
                "title": doc.title,
                "fields": fields
            }, status=200)

        return Response(serializer.errors, status=400)
