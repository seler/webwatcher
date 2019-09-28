from django.db import models
from django.utils.translation import ugettext_lazy as _

from .parser import get_parser_name_by_url, get_parser_by_name


class Watch(models.Model):
    user = models.ForeignKey(
        "auth.User", verbose_name=_("user"), on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    url = models.CharField(max_length=255, verbose_name=_("url"))
    _parser = models.CharField(max_length=255, blank=True, editable=False)

    periodic_task = models.OneToOneField(
        "django_celery_beat.PeriodicTask", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _(u"watch")
        verbose_name_plural = _(u"watches")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self._parser:
            self._parser = get_parser_name_by_url(self.url)
        return super().save(*args, **kwargs)

    @property
    def parser(self):
        if self._parser:
            ParserClass = get_parser_by_name(self._parser)
            return ParserClass(self)


class Item(models.Model):
    watch = models.ForeignKey(Watch, verbose_name=_("watch"), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_("title"))
    link = models.CharField(max_length=255, verbose_name=_("link"))
    description = models.TextField(verbose_name=_("description"))
    uid = models.CharField(max_length=255, verbose_name=_("unique id"))
    timestamp = models.DateTimeField(verbose_name=_("timestamp"))
    image = models.CharField(max_length=255, verbose_name=_("image"))

    class Meta:
        verbose_name = _(u"item")
        ordering = ("-timestamp",)
        verbose_name_plural = _(u"items")

    def __str__(self):
        return self.title
