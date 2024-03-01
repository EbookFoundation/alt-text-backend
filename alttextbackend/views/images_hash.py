from rest_framework import serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

import alttextbackend.data.postgres.images as images


class GetImagesByHashSerializer(serializers.Serializer):
    hash = serializers.CharField(required=True)


class ImagesHashView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = GetImagesByHashSerializer

    def get(self, request, *args, **kwargs):
        image_hash = kwargs.get("hash")
        data = {"hash": image_hash}
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        imgs = images.getImagesByHash(image_hash)

        return Response(map(images.jsonifyImage, imgs), status=status.HTTP_200_OK)
