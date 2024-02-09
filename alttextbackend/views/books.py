from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uuid import uuid4


class GetBooksSerializer(serializers.Serializer):
    titleQ = serializers.CharField(required=False)
    authorQ = serializers.CharField(required=False)
    sortBy = serializers.ChoiceField(choices=['title', 'author'], style={'base_template': 'radio.html'}, default = 'title')
    sortOrder = serializers.ChoiceField(choices=['asc', 'desc'], style={'base_template': 'radio.html'}, default = 'asc')
    limit = serializers.IntegerField(min_value=1, required=False)
    skip = serializers.IntegerField(min_value=0, required=False)

class AddBookSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False)
    author = serializers.CharField(required=True, allow_blank=False)
    description = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField(required=True)
    cover = serializers.ImageField(required=False)

class BooksView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = AddBookSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetBooksSerializer
        elif self.request.method == 'POST':
            return AddBookSerializer
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Access validated data
        validated_data = serializer.validated_data
        title_query = validated_data.get('titleQ')
        author_query = validated_data.get('authorQ')
        sort_by = validated_data.get('sortBy')
        sort_order = validated_data.get('sortOrder')
        limit = validated_data.get('limit')
        skip = validated_data.get('skip')

        # TODO: perform logic

        # TODO: return books
        return Response(validated_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # validate request data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # perform initial book processing
        file = validated_data["file"]
        if not file.name.endswith(".zip"):
            return Response(
                {"file": ["file must be a zip"]}, status=status.HTTP_400_BAD_REQUEST
            )
        id = uuid4()
        books_path = "./books/"
        default_storage.save(f"{books_path}{str(id)}.zip", ContentFile(file.read()))

        # TODO: ensure book has valid root html file

        # TODO: analyze book and images, store them in database

        # save cover image
        covers_path = "./covers/"
        default_storage.save(
            f"{covers_path}{str(id)}.{validated_data['cover'].name.split('.')[-1]}",
            ContentFile(validated_data["cover"].read()),
        )

        return Response(
            {
                "book": validated_data.get("title"),
                "description": validated_data.get("description"),
            },
            status=status.HTTP_201_CREATED,
        )
