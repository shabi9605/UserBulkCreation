# Generated by Django 5.1.4 on 2024-12-31 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkUploadLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='user_files/')),
                ('response', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
