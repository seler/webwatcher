from django.db import models
from django.utils.translation import ugettext_lazy as _

from .parser import get_parser_by_url


class Page(models.Model):

    user = models.ForeignKey("auth.User", verbose_name=_("user"), on_delete="delete")
    name = models.CharField(max_length=255, verbose_name=_("name"))
    url = models.CharField(max_length=255, verbose_name=_("url"))
    parser = models.CharField(max_length=255, verbose_name=_("parser"), blank=True)

    class Meta:
        verbose_name = _(u"page")
        verbose_name_plural = _(u"pages")
        ordering = []
        get_latest_by = ""

    def __unicode__(self):
        return ""

    def save(self, *args, **kwargs):
        if not self.parser:
            self.parser = get_parser_by_url(self.url)
        return super().save(*args, **kwargs)
