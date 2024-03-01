import sys

import alttextbackend.data.postgres.books as books
import alttextbackend.data.postgres.images as images
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

sys.path.append("../")


class ImagesFromBookSerializer(serializers.Serializer):
    bookid = serializers.CharField(required=True)


class BooksBookidImagesView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = ImagesFromBookSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={"bookid": kwargs.get("bookid")})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        id = validated_data.get("bookid")

        # check if book exists in database
        book = books.getBook(id)
        if not book:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # get images from database
        imgs = images.getImagesByBook(id)

        return Response(map(images.jsonifyImage, imgs), status=status.HTTP_200_OK)
