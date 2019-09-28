from celery import shared_task
from .models import Watch, Item


@shared_task
def check(watch_id):
    watch = Watch.objects.get(pk=watch_id)
    items = list(watch.parser.get_items())
    uids = [item.uid for item in items]
    existing_uids = Item.objects.filter(uid__in=uids).values_list("uid", flat=True)
    to_save = [item for item in items if item.uid not in existing_uids]
    if to_save:
        saved = Item.objects.bulk_create(to_save)
        # todo: send email/notification
        return len(saved)
