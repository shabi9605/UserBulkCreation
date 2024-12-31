from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import parsers
from .models import User, BulkUploadLogs
from .serializers import FileBackgroundUploadSerializer, FileUploadSerializer, UserSerializer 
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
    
    
    

class UploadBulkDataViewSet(viewsets.ModelViewSet):
    serializer_class = FileBackgroundUploadSerializer
    queryset = BulkUploadLogs.objects.filter()
    permission_classes = []
    
    @action(
        methods=["post"],
        detail=False,
        serializer_class=FileBackgroundUploadSerializer,  # Serializer used for the custom action
        url_path="bulk-upload-background",  # URL path for this action
        parser_classes=[parsers.MultiPartParser],  # Allow handling file uploads
    )
    def upload_bulk_users_background(self, request, *args, **kwargs):
        """
        Custom action to handle bulk user uploads in the background.

        Accepts a file upload, validates it, and processes it using the serializer.
        """
        # Deserialize and validate the incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the uploaded data (handled by the serializer)
        data = serializer.save()

        # Return a success response
        return Response({'results': "File uploaded successfully"})
