from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uuid import uuid4

class BooksBookidView(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request, *args, **kwargs):
        return Response({"TODO": "TODO"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response({"TODO": "TODO"}, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        return Response({"TODO": "TODO"}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        return Response({"TODO": "TODO"}, status=status.HTTP_200_OK)
