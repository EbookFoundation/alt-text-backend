import sys
import zipfile
from uuid import uuid4

import alttextbackend.data.analyze as analyze
import alttextbackend.data.postgres.books as books
import alttextbackend.data.postgres.images as images
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

sys.path.append("../")


class GetBooksSerializer(serializers.Serializer):
    titleQ = serializers.CharField(required=False)
    limit = serializers.IntegerField(min_value=1, required=False)
    skip = serializers.IntegerField(min_value=0, required=False)


class AddBookSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField(required=True, allow_blank=False)
    book = serializers.FileField(required=True)
    cover = serializers.ImageField(required=False)


class BooksView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = AddBookSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetBooksSerializer
        elif self.request.method == "POST":
            return AddBookSerializer
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Access validated data
        validated_data = serializer.validated_data
        titleQ = validated_data.get("titleQ", None)
        limit = validated_data.get("limit", None)
        skip = validated_data.get("skip", None)

        # get array of books
        result = books.getBooks(titleQ, limit, skip)

        return Response(map(books.jsonifyBook, result), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # validate request data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        id = validated_data.get("id", uuid4())
        # check if id is already in use
        book = books.getBook(id)
        if book:
            return Response(
                {"error": "id already in use"}, status=status.HTTP_400_BAD_REQUEST
            )

        # perform initial book processing
        file = validated_data["book"]
        if not file.name.endswith(".zip"):
            return Response(
                {"file": ["file must be a zip"]}, status=status.HTTP_400_BAD_REQUEST
            )
        book_path = f"./books/{str(id)}"
        default_storage.save(f"{book_path}.zip", ContentFile(file.read()))
        with zipfile.ZipFile(default_storage.path(f"{book_path}.zip"), "r") as zip_ref:
            zip_ref.extractall(default_storage.path(f"{book_path}"))
        default_storage.delete(f"{book_path}.zip")

        # ensure book has valid root html file
        html_file = analyze.findHTML(book_path)
        if html_file == None:
            default_storage.delete(book_path)
            return Response(
                {"error": "No HTML file found in the extracted folder"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # save cover image
        coverExt = None
        if "cover" in validated_data and validated_data["cover"] is not None:
            coverExt = validated_data["cover"].name.split(".")[-1]
            default_storage.save(
                f"./covers/{str(id)}.{coverExt}",
                ContentFile(validated_data["cover"].read()),
            )

        alt = analyze.createAnalyzer()
        alt.parseFile(html_file)
        # store basic book info into database
        size = analyze.getSize(book_path)
        imgs = alt.getAllImgs()
        books.addBook(
            title=validated_data["title"],
            size=str(size),
            numImages=len(imgs),
            id=id,
            coverExt=coverExt,
        )
        # store info for all images in database
        for img in imgs:
            context = alt.getContext(img)
            thisHash = hash(alt.getImgData(img["src"]))
            images.addImage(
                bookid=id,
                src=img["src"],
                hash=thisHash,
                alt=img["alt"],
                originalAlt=img["alt"],
                beforeContext=context[0],
                afterContext=context[1],
            )

        book = books.getBook(id)
        return Response(
            books.jsonifyBook(book),
            status=status.HTTP_201_CREATED,
        )
