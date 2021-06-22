# Generated by Django 3.1.7 on 2021-05-09 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskresult",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="Datetime field when the task was created(in UTC).",
                null=True,
                verbose_name="Created datetime",
            ),
        ),
    ]
