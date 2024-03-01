import copy
import os
import shutil
import threading
import time

import alttextbackend.data.analyze as analyzer
import alttextbackend.data.postgres.books as books
import alttextbackend.data.postgres.images as images
from django.core.files.storage import default_storage
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.base import ContentFile


class GetBookSerializer(serializers.Serializer):
    bookid = serializers.CharField(required=True)


class UpdateBookSerialzer(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_blank=False)
    cover = serializers.ImageField(required=False)


class AnalyzeBookSerializer(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    missingOnly = serializers.BooleanField(required=False, default=True)
    waitForAnalysis = serializers.BooleanField(required=False, default=False)


class DeleteBookSerializer(serializers.Serializer):
    bookid = serializers.CharField(required=True)


class BooksBookidView(APIView):
    parser_classes = (FormParser, MultiPartParser)

    serializer_class = UpdateBookSerialzer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetBookSerializer
        elif self.request.method == "PATCH":
            return UpdateBookSerialzer
        elif self.request.method == "PUT":
            return AnalyzeBookSerializer
        elif self.request.method == "DELETE":
            return DeleteBookSerializer
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data={"bookid": kwargs.get("bookid")})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # get book from database
        book = books.getBook(validated_data.get("bookid"))
        if not book:
            return Response(
                {"error": "No book of that id was found in database."},
                status=status.HTTP_404_BAD_REQUEST,
            )

        return Response(books.jsonifyBook(book), status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = request.data
        data["bookid"] = kwargs.get("bookid")
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # check if book exists in database
        book = books.getBook(validated_data.get("bookid"))
        if not book:
            return Response(
                {"error": "No book of that id was found in database."},
                status=status.HTTP_404_BAD_REQUEST,
            )
        book = books.jsonifyBook(book)

        # update book title and cover
        title = validated_data.get("title", None)
        coverExt = None
        if "cover" in validated_data and validated_data["cover"] is not None:
            coverExt = validated_data["cover"].name.split(".")[-1]
            default_storage.delete(
                f"./covers/{str(validated_data.get('bookid'))}.{book['coverExt']}"
            )
            default_storage.save(
                f"./covers/{str(validated_data.get('bookid'))}.{coverExt}",
                ContentFile(validated_data["cover"].read()),
            )

        books.updateBook(validated_data.get("bookid"), title=title, coverExt=coverExt)

        book = books.jsonifyBook(books.getBook(validated_data.get("bookid")))

        return Response(book, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        data = copy.deepcopy(request.query_params)
        data["bookid"] = kwargs.get("bookid")
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        bookid = validated_data.get("bookid")
        # check for book's existence
        book = books.getBook(bookid)
        if not book:
            return Response(
                {"error": "Book not found in database."},
                status=status.HTTP_404_BAD_REQUEST,
            )

        html_file = analyzer.findHTML(f"./books/{str(validated_data.get('bookid'))}")
        if html_file == None:
            return Response(
                {"error": "Failed to find HTML file in book directory."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        alt = analyzer.createAnalyzer()
        alt.parseFile(html_file)
        imgs = []
        if validated_data.get("missingOnly"):
            imgs = alt.getNoAltImgs()
        else:
            imgs = alt.getAllImgs()

        # set book and all images to "processing" status
        if validated_data.get("waitForAnalysis"):
            analyzer.analyzeImagesV2(alt, imgs, bookid)
        else:
            threading.Thread(
                target=analyzer.analyzeImagesV2, args=(alt, imgs, bookid)
            ).start()

        book = books.jsonifyBook(books.getBook(bookid))
        if not validated_data.get("waitForAnalysis"):
            book["status"] = "processing"

        return Response(book, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data={"bookid": kwargs.get("bookid")})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        # check for book's existence
        book = books.getBook(validated_data.get("bookid"))
        if not book:
            return Response(
                {"error": "Book not found in database."},
                status=status.HTTP_404_BAD_REQUEST,
            )
        book = books.jsonifyBook(book)
        book["status"] = "deleted"

        # delete book from table (this cascades to images table as well)
        books.deleteBook(validated_data.get("bookid"))

        # delete book directory and cover image
        try:
            folder_path = f"./books/{str(validated_data.get('bookid'))}"
            if default_storage.exists(folder_path):
                shutil.rmtree(default_storage.path(folder_path))
                if book["coverExt"]:
                    try:
                        default_storage.delete(
                            f"./covers/{str(validated_data.get('bookid'))}.{book['coverExt']}"
                        )
                    except:
                        return Response(
                            {"error": "Failed to delete cover image."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
            else:
                return Response(
                    {"error": "Failed to find book directory."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except Exception:
            return Response(
                {"error": "Failed to delete book directory."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            book,
            status=status.HTTP_200_OK,
        )
