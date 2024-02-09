from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uuid import uuid4

class GetImagesByHashSerializer(serializers.Serializer):
    hash = serializers.CharField(required=True)

class ImagesHashView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = GetImagesByHashSerializer

    def get(self, request, *args, **kwargs):
        image_hash = kwargs.get('hash')
        data = {'hash': image_hash}
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: IMPLEMENT LOGIC

        return Response(data, status=status.HTTP_200_OK)
