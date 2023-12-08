from django.core.mail import send_mail
from django.conf import settings
import random
import string



def send_email_to_client(message_to, to_besent):
    pass
    # subject = 'Credentails Details for Your login'
    # message = message_to
    # from_email = settings.EMAIL_HOST_USER
    # recipient = [to_besent]
    # send_mail(subject,message,from_email,recipient)

def random_passowrd():
    characters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(characters) for i in range(8))
    # print("Random password is:", password)
    return password