# Generated by Django 2.2.5 on 2019-10-03 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("webwatcher", "0007_auto_20191003_1458")]

    operations = [
        migrations.AlterField(
            model_name="watch",
            name="url",
            field=models.URLField(max_length=512, verbose_name="url"),
        )
    ]
