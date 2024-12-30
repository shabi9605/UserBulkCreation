from rest_framework import serializers
from .models import User
import pandas as pd
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "age"]
        required_fields = ["name", "email", "age"]


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    REQUIRED_COLUMNS = {"name", "email", "age"}

    def validate(self, data):
        # Read the uploaded CSV file
        try:
            csv_file_data = pd.read_csv(data["file"])
        except Exception as e:
            raise ValidationError(
                f"Unable to read the file. Ensure it is a valid CSV. Error: {str(e)}"
            )

        # Get the column headers, normalize them (lowercase and strip)
        column_headers = set(header.lower().strip() for header in csv_file_data.columns)

        # Find missing columns
        missing_columns = self.REQUIRED_COLUMNS - column_headers
        if missing_columns:
            raise ValidationError(
                f"The following required columns are missing: {', '.join(missing_columns)}"
            )
        data["csv_file_data"] = csv_file_data
        return data

    def create(self, validated_data):
        """
        Process the CSV data, validate each row, and save valid records to the database.
        """
        csv_file_data = validated_data["csv_file_data"]
        created_users = []
        rejected_reasons = []

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
                user_data["age"] = int(user_data["age"])

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
        return return_response
