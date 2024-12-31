from celery import shared_task
import pandas as pd
import json

@shared_task
def create_users(csv_file_data_json, instance_id):
    from .serializers import UserSerializer
    from .models import BulkUploadLogs
    bulk_upload_log = BulkUploadLogs.objects.get(id=instance_id)
    created_users = []
    rejected_reasons = []

    # Deserialize the JSON string back to a list of dictionaries
    csv_file_data = pd.DataFrame(json.loads(csv_file_data_json))

    total_rows = csv_file_data.shape[0]
    for index, row in csv_file_data.iterrows():
        # Prepare user data
        user_data = {
            "name": str(row.get("Name", "")).strip() if isinstance(row.get("Name", ""), str) else "",
            "email": str(row.get("Email", "")).strip() if isinstance(row.get("Email", ""), str) else "",
            "age": row.get("Age"),
        }

        # Convert age to integer if it's not null or NaN
        if user_data["age"] is not None and pd.notna(user_data["age"]):
            try:
                user_data["age"] = int(user_data["age"])
            except ValueError:
                user_data["age"] = None  # Set to None if the conversion fails

        # Use UserSerializer for validation and object creation
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user to the database
            created_users.append(user)
        else:
            error_obj = {
                key: [str(err) for err in serializer.errors.get(key, [])]
                for key in serializer.errors
            }
            rejected_reasons.append(f"Error at row {index + 1}: {error_obj}")

    return_response = {
        "total_records_saved": len(created_users),
        "total_records_rejected": total_rows - len(created_users),
        "rejected_records": rejected_reasons,
    }
    bulk_upload_log.response = return_response
    bulk_upload_log.status = True
    bulk_upload_log.save()
    return return_response
