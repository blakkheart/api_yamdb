from django.core.mail import send_mail


def send_email_to_user(email, code):
    send_mail(
        subject='Confirm your registration on YaMDB',
        message=f'Your confirmation code: {code}',
        from_email='yamdb_registration@yandex.ru',
        recipient_list=[email],
        fail_silently=True,
    )
