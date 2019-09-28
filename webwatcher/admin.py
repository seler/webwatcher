from django.contrib import admin
from .models import Watch, Item
from django.utils.safestring import mark_safe


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    pass


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
