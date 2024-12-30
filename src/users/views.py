from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import parsers
from .models import User
from .serializers import FileUploadSerializer, UserSerializer
from rest_framework.decorators import action
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    permission_classes = []

    @action(
        methods=["post"],
        detail=False,
        serializer_class=FileUploadSerializer,
        url_path="bulk-upload",
        parser_classes=[parsers.MultiPartParser],
    )
    def upload_bulk_users(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)
