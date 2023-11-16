from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    bookdata = serializers.CharField()


class ImageSerializer(serializers.Serializer):
    imagedata = serializers.CharField()
    beforeContext = serializers.CharField(required=False)
    afterContext = serializers.CharField(required=False)


class BooksView(APIView):
    def get(self, request, *args, **kwargs):
        data = {"books": "this is a book"}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            return Response(
                {"book": validated_data.get("bookdata")},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImagesView(APIView):
    def get(self, request, *args, **kwargs):
        data = {"images": "this is an image"}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            res = {"book": validated_data.get("imagedata")}
            if validated_data.get("beforeContext"):
                res["beforeContext"] = validated_data.get("beforeContext")
            if validated_data.get("afterContext"):
                res["afterContext"] = validated_data.get("afterContext")
            return Response(
                res,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
