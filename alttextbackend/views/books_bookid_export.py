from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uuid import uuid4

class ExportBookSerializer(serializers.Serializer):
    bookid = serializers.CharField(required=True)

class BooksBookidExportView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = ExportBookSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={"bookid": kwargs.get('bookid')})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # TODO: IMPLEMENT LOGIC

        return Response(validated_data, status=status.HTTP_200_OK)
