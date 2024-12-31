from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd
from .tasks import create_users
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    age = models.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(0)])

    def __str__(self):
        return str(self.id)


class BulkUploadLogs(models.Model):
    file = models.FileField(upload_to='user_files/')
    response = models.JSONField(null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    

@receiver(post_save, sender=BulkUploadLogs)
def uploa_users(sender, instance, created, **kwargs):
    if created:
        csv_file_data = pd.read_csv(instance.file)
        csv_file_data_json = csv_file_data.to_json(orient="records")
        create_users.delay(csv_file_data_json, instance.id)