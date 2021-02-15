from .models import Product, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime


def week_mailing():
    sub_list = Subscriber.objects.all()
    email = [user.username.email for user in sub_list]
    week_date = datetime.date.today() - datetime.timedelta(days=7)
    product_list = Product.objects.filter(date__gte=week_date)
    html_content = render_to_string(
        'email_temlates/week_new.html',
        {'product_list': product_list}
    )
    msg = EmailMultiAlternatives(
        subject='New in the site',
        from_email='from@example.com',
        to=email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()