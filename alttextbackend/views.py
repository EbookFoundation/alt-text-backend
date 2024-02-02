from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uuid import uuid4


class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    cover = serializers.ImageField()
    file = serializers.FileField()


class BooksView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        # TODO: get's list of books given limits
        data = {"books": []}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # validate request data
        serializer = self.serializer_class(data=request.data)
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


# class ImageSerializer(serializers.Serializer):
#     imagedata = serializers.CharField()
#     beforeContext = serializers.CharField(required=False)
#     afterContext = serializers.CharField(required=False)

# class ImagesView(APIView):
#     def get(self, request, *args, **kwargs):
#         data = {"images": "this is an image"}
#         return Response(data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             validated_data = serializer.validated_data
#             res = {"book": validated_data.get("imagedata")}
#             if validated_data.get("beforeContext"):
#                 res["beforeContext"] = validated_data.get("beforeContext")
#             if validated_data.get("afterContext"):
#                 res["afterContext"] = validated_data.get("afterContext")
#             return Response(
#                 res,
#                 status=status.HTTP_201_CREATED,
#             )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
