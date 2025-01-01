import pytest
import csv
from io import StringIO
from django.urls import reverse
from rest_framework import status
from users.models import User  # Adjust according to your actual model path

@pytest.mark.django_db
def test_upload_bulk_users_valid_csv(client):  # Use 'client' instead of 'api_client'
    user_viewset_url = reverse('users-management-list')  # Use the correct URL name
    valid_csv = StringIO()
    writer = csv.writer(valid_csv)
    writer.writerow(['username', 'email', 'password'])
    writer.writerow(['user1', 'user1@example.com', 'password123'])
    writer.writerow(['user2', 'user2@example.com', 'password123'])

    valid_csv.seek(0)

    response = client.post(
        user_viewset_url,
        {'file': valid_csv},
        format='multipart'
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 2
    assert User.objects.filter(username='user1').exists()
    assert User.objects.filter(username='user2').exists()

@pytest.mark.django_db
def test_upload_bulk_users_invalid_csv(client):  # Use 'client' instead of 'api_client'
    # Your test logic for invalid CSV file goes here
    pass

@pytest.mark.django_db
def test_upload_bulk_users_no_file(client):  # Use 'client' instead of 'api_client'
    # Your test logic for no file goes here
    pass
