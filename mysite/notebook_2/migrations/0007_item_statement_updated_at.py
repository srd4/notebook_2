# Generated by Django 4.1.2 on 2022-12-16 04:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notebook_2', '0006_rename_itemstatementversion_statementversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='statement_updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
