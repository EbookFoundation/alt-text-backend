from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uuid import uuid4

class GetImageBySrc(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    src = serializers.CharField(required=True)

class UpdateImageBySrc(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    src = serializers.CharField(required=True)
    alt = serializers.CharField(required=True)
    beforeContext = serializers.CharField(required=False)
    afterContext = serializers.CharField(required=False)

class AnalyzeImageBySrc(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    src = serializers.CharField(required=True)

class BooksBookidImageView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetImageBySrc
        elif self.request.method == 'PATCH':
            return UpdateImageBySrc
        elif self.request.method == 'PUT':
            return AnalyzeImageBySrc
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = request.query_params
        data['bookid'] = kwargs.get('bookid')
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # TODO: IMPLEMENT LOGIC

        return Response(validated_data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = request.data
        data.update(request.query_params)
        data['bookid'] = kwargs.get('bookid')
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # TODO: IMPLEMENT LOGIC

        return Response(validated_data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = request.query_params
        data['bookid'] = kwargs.get('bookid')
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # TODO: IMPLEMENT LOGIC

        return Response(validated_data, status=status.HTTP_200_OK)
