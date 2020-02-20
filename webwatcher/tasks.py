from celery import shared_task

from .models import Item, Watch
from .sendmail import sendmail


def _get_new_items(watch):
    items = list(watch.parser.get_items())
    uids = [item.uid for item in items]
    existing_uids = Item.objects.filter(uid__in=uids).values_list("uid", flat=True)
    new_items = [item for item in items if item.uid not in existing_uids]
    return new_items


@shared_task
def check(watch_id):
    watch = Watch.objects.get(pk=watch_id)
    new_items = _get_new_items(watch)
    if new_items:
        saved = Item.objects.bulk_create(new_items)
        if watch.notification == watch.NOTIFICATION_INSTANT:
            sendmail(watch.user, watch, saved)
        return len(saved)
