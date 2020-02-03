# Generated by Django 2.2.5 on 2019-09-28 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_celery_beat", "0011_auto_20190508_0153"),
        ("webwatcher", "0003_item_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="item",
            options={
                "ordering": ("-timestamp",),
                "verbose_name": "item",
                "verbose_name_plural": "items",
            },
        ),
        migrations.AddField(
            model_name="watch",
            name="periodic_task",
            field=models.OneToOneField(
                default=1, on_delete="delete", to="django_celery_beat.PeriodicTask"
            ),
            preserve_default=False,
        ),
    ]
