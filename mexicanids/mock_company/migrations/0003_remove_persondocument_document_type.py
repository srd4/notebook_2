# Generated by Django 4.1.2 on 2022-12-07 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mock_company', '0002_remove_person_drivers_license_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persondocument',
            name='document_type',
        ),
    ]
