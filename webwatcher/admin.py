from django.contrib import admin
from .models import Watch, Item
from django.utils.safestring import mark_safe
from django import forms
from django_celery_beat.models import PeriodicTask
from django.forms.models import fields_for_model

periodic_task_field_names = ["interval", "crontab", "solar", "clocked", "enabled"]
periodic_task_fields = fields_for_model(PeriodicTask, fields=periodic_task_field_names)


class WatchForm(forms.ModelForm):
    interval = periodic_task_fields["interval"]
    crontab = periodic_task_fields["crontab"]
    solar = periodic_task_fields["solar"]
    clocked = periodic_task_fields["clocked"]
    enabled = periodic_task_fields["enabled"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "instance" in kwargs and kwargs["instance"] is not None:
            for field in periodic_task_field_names:
                self.fields[field].initial = getattr(
                    kwargs["instance"].periodic_task, field
                )

    class Meta:
        """Form metadata."""

        model = Watch
        fields = "__all__"


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    form = WatchForm
    fieldsets = (
        (
            None,
            {
                "fields": ("user", "name", "url", "parser_display"),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Schedule",
            {"fields": periodic_task_field_names, "classes": ("extrapretty", "wide")},
        ),
    )
    readonly_fields = ["parser_display"]

    def parser_display(self, obj):
        return obj.parser.name

    def save_model(self, request, obj, form, change):
        if obj.periodic_task_id is None:
            periodic_task = PeriodicTask()
        else:
            periodic_task = obj.periodic_task
        periodic_task.name = obj.name
        periodic_task.task = "webwatcher.tasks.check"
        for field in periodic_task_field_names:
            setattr(periodic_task, field, form.cleaned_data[field])
        periodic_task.save()
        obj.periodic_task_id = periodic_task.id
        obj.save()
        periodic_task.args = f"[{obj.id}]"
        periodic_task.save()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = (
        "admin_image",
        "title",
        "link",
        "watch",
        "content",
        "uid",
        "timestamp",
    )
    list_display = ("admin_image", "title", "link", "watch", "timestamp")

    def content(self, obj):
        return mark_safe(obj.description)

    content.allow_tags = True
    content.short_description = "content"

    def admin_image(self, obj):
        return mark_safe(f'<img src="{obj.image}" style="height: 100px"/>')

    admin_image.allow_tags = True
    admin_image.short_description = "image"
