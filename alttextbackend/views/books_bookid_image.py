import copy
import threading

import alttextbackend.data.analyze as analyze
import alttextbackend.data.postgres.books as books
import alttextbackend.data.postgres.images as images
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class GetImageBySrc(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    src = serializers.CharField(required=True)


class UpdateImageBySrc(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    src = serializers.CharField(required=True)
    alt = serializers.CharField(required=True)
    beforeContext = serializers.CharField(required=False)
    afterContext = serializers.CharField(required=False)
    additionalContext = serializers.CharField(required=False)


class AnalyzeImageBySrc(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    src = serializers.CharField(required=True)
    waitForAnalysis = serializers.BooleanField(required=False, default=False)


class BooksBookidImageView(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetImageBySrc
        elif self.request.method == "PATCH":
            return UpdateImageBySrc
        elif self.request.method == "PUT":
            return AnalyzeImageBySrc
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = copy.deepcopy(request.query_params)
        data["bookid"] = kwargs.get("bookid")
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # check if book exists in database
        book = books.getBook(validated_data.get("bookid"))
        if not book:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # get image from database
        img = images.getImageByBook(
            validated_data.get("bookid"), validated_data.get("src")
        )
        if img == None:
            return Response(
                {"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            images.jsonifyImage(img),
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = copy.deepcopy(request.data)
        data.update(request.query_params)
        data["bookid"] = kwargs.get("bookid")
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        alt = validated_data.get("alt", None)
        beforeContext = validated_data.get("beforeContext", None)
        afterContext = validated_data.get("afterContext", None)
        additionalContext = validated_data.get("additionalContext", None)

        img = images.getImageByBook(
            validated_data.get("bookid"), validated_data.get("src")
        )
        if img == None:
            return Response(
                {"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # update image in database
        images.updateImage(
            bookid=validated_data.get("bookid"),
            src=validated_data.get("src"),
            alt=alt,
            beforeContext=beforeContext,
            afterContext=afterContext,
            additionalContext=additionalContext,
        )

        img = images.getImageByBook(
            validated_data.get("bookid"), validated_data.get("src")
        )

        return Response(images.jsonifyImage(img), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = copy.deepcopy(request.query_params)
        data["bookid"] = kwargs.get("bookid")
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # find HTML file
        bookid = str(validated_data.get("bookid"))
        html_file = analyze.findHTML(f"./books/{bookid}")
        if html_file == None:
            return Response(
                {"error": "Failed to find HTML file in book directory."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # generate alt for image
        alt = analyze.createAnalyzer()
        alt.parseFile(html_file)
        img = alt.getImg(validated_data.get("src"))
        if img == None:
            return Response(
                {"error": "Failed to find image in book."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if validated_data.get("waitForAnalysis"):
            analyze.analyzeSingularImageV2(alt, img, bookid)
        else:
            threading.Thread(
                target=analyze.analyzeSingularImageV2, args=(alt, img, bookid)
            ).start()

        image = images.jsonifyImage(
            images.getImageByBook(
                validated_data.get("bookid"), validated_data.get("src")
            )
        )

        if not validated_data.get("waitForAnalysis"):
            image["status"] = "processing"

        return Response(image, status=status.HTTP_200_OK)
