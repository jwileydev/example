# Generated by Django 4.1.3 on 2022-12-04 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("example_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="productuserengagement",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]