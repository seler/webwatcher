from django.template import loader
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def sendmail(user, watch, items):
    html_template = loader.get_template("webwatcher/email_notification.html")
    plain_template = loader.get_template("webwatcher/email_notification.txt")
    context = {"user": user, "items": items}
    html_content = html_template.render(context)
    text_content = plain_template.render(context)

    subject = f"[WebWatcher] {watch.name}"
    msg = EmailMultiAlternatives(
        subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
