# Generated by Django 4.1.2 on 2022-12-07 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('passport', models.FileField(upload_to='pasaportes')),
                ('identity_document', models.FileField(upload_to='cedulas')),
                ('drivers_license', models.FileField(upload_to='licencias')),
            ],
        ),
    ]
