from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from legendarymotosports._celery import app

# ********** EMAIL FUNCS ********** #


def send_activation_code(email, activation_code):
    title = "Welcome to Legendary Motosport!"
    msg = (
        "You are now in just one step to become an owner of a dream car, \n"
        "just press the button below or enter this code on site:"
    )
    context = {
        "title": title,
        "text_detail": msg,
        "domain": "http://localhost:8000",
        "email": email,
        "activation_code": activation_code,
    }
    msg_html = render_to_string("accounts/email.html", context=context)
    message = strip_tags(msg_html)
    send_mail(
        title,
        message,
        "bazinga3469@gmail.com",
        [email],
        html_message=msg_html,
        fail_silently=False
    )

