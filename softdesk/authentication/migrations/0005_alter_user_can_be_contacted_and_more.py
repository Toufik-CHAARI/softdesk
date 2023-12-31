# Generated by Django 4.2.6 on 2023-10-22 13:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0004_alter_user_can_be_contacted_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="can_be_contacted",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="can_data_be_shared",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="consent_choice",
            field=models.BooleanField(default=False),
        ),
    ]
