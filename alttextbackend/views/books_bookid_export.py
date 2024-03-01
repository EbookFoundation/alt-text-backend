import copy
import os
import shutil
import zipfile

import alttextbackend.data.analyze as analyze
import alttextbackend.data.postgres.books as books
import alttextbackend.data.postgres.images as images
from django.core.files.storage import default_storage
from django.http import HttpResponse
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class ExportBookSerializer(serializers.Serializer):
    bookid = serializers.CharField(required=True)
    name = serializers.CharField(required=False)


class BooksBookidExportView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = ExportBookSerializer

    def get(self, request, *args, **kwargs):
        data = copy.deepcopy(request.query_params)
        data["bookid"] = kwargs.get("bookid")
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        bookid = validated_data.get("bookid")
        # check if book exists in database
        book = books.getBook(bookid)
        if not book:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # find HTML file
        bookid = str(validated_data.get("bookid"))
        html_file = analyze.findHTML(f"./books/{bookid}")
        if html_file == None:
            return Response(
                {"error": "Failed to find HTML file in book directory."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # get all image tags in book
        alt = analyze.createAnalyzer()
        alt.parseFile(html_file)
        imgs = alt.getAllImgs()
        for img in imgs:
            databaseImg = images.jsonifyImage(images.getImageByBook(bookid, img["src"]))
            alt.setAlt(img["src"], databaseImg["alt"])

        try:
            shutil.copytree(
                default_storage.path(f"./books/{bookid}"), f"./books/{bookid}-t"
            )
        except Exception as e:
            return Response(
                {"error": "Failed to copy book into temp folder."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        html_file = analyze.findHTML(f"./books/{bookid}-t")
        if html_file == None:
            return Response(
                {"error": "Failed to find HTML file in temp book directory."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        default_storage.delete(html_file)
        alt.exportToFile(html_file)

        # Zip the temp folder
        zip_filename = f"./books/{bookid}-t.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for root, _, files in os.walk(f"./books/{bookid}-t"):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(
                            os.path.join(root, file), f"./books/{bookid}-t"
                        ),
                    )

        # Send the zip file as a response
        filename = validated_data.get("name", f"{bookid}")
        print(filename)
        response = None
        with open(zip_filename, "rb") as f:
            response = HttpResponse(f, content_type="application/zip")
            response["Content-Disposition"] = f"attachment; filename={filename}.zip"

        # Delete the temp zip and folder
        os.remove(zip_filename)
        shutil.rmtree(f"./books/{bookid}-t")

        return response
