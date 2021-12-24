from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser


# ********** EMAIL FUNCS ********** #
# def send_activation_code(email, activation_code):
#     title = "Welcome to Legendary Motosport!"
#     msg = (
#         "You are now in just one step to become an owner of a dream car, \n"
#         "just press the button below or enter this code on site:"
#     )
#     context = {
#         "title": title,
#         "text_detail": msg,
#         "domain": "http://localhost:8000",
#         "email": email,
#         "activation_code": activation_code,
#     }
#     msg_html = render_to_string("accounts/email.html", context=context)
#     message = strip_tags(msg_html)
#     send_mail(
#         title,
#         message,
#         "bazinga3469@gmail.com",
#         [email],
#         html_message=msg_html,
#         fail_silently=False
#     )


# def send_manufacturer_confirm(email, manufacturer_code):
#     title = "New Manufacturer arrives!"
#     msg = (
#         "A new manufacturer wants to become part of Legendary Motosport, \n"
#         "press the button below to let him in, or ignore message if you dont like him or shomething:"
#     )
#     context = {
#         "title": title,
#         "text_detail": msg,
#         "domain": "http://localhost:8000",
#         "manufacturer_code": manufacturer_code,
#         "email": email,
#     }
#     msg_html = render_to_string("accounts/email.html", context=context)
#     message = strip_tags(msg_html)
#     send_mail(
#         title,
#         message,
#         "bazinga3469@gmail.com",
#         ["bazinga3469@gmail.com"],
#         html_message=msg_html,
#         fail_silently=False,
#     )


# ********** END EMAIL FUNCS ********** #


# ********** USER FUNCS ********** #

def get_user(request):
    """
    Returns user object and user data to display
    """
    from django.contrib.auth.models import AnonymousUser
    token = request.COOKIES.get('auth_token')
    if token:
        try:
            user = CustomUser.objects.get(auth_token=token)
        except ObjectDoesNotExist:
            user = AnonymousUser()
    else:
        user = AnonymousUser()
    
    
    if isinstance(user, AnonymousUser):
        user.username = "AnonymousUser"
        # user_data = dict(
        #     email=user.email,
        #     username=user.username,
        #     image=user.image,
        #     is_authenticated=bool(user.is_active),
        #     is_manufacturer=user.is_manufacturer,
        # )
    # else:
    #     user_data = dict(
    #         email=None,
    #         username='AnonymousUser',
    #         image=None,
    #         is_authenticated=False,
    #         is_manufacturer=False,
    #     )
    return user

# ********** END USER FUNCS ********** #
