from ctypes import resize
from django.conf import settings
from django.core.mail import send_mail
from ..models import Trainee


def sendToReceipnt(to, head, body):
    subject = head
    message = body
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to, ]
    try:
        x = send_mail(subject, message, email_from, recipient_list)
        print("$$$$$$$$$$$$$$$$")
        print(x)
    except Exception as e:
        print("!!!!!!!!!!!!>Error In sending Mail to Receipnt")
        print(e)

def sendToAll(head, body, fid):
    data = []
    recipient_list = []
    res = False
    try:
        trainee_list = Trainee.objects.filter(fid=fid)
        for trainee in trainee_list:
            data.append({
                'name': trainee.trainee_name,
                'domain': trainee.trainee_domain,
            })

            recipient_list.append(trainee.trainee_email)
    except Exception as e:
        print("!!!!!!!!!!!!>Error In getting data for sending email to all")
        print(e)
        return res

    for cnt,d in enumerate(data, 0):
        message = ''
        message = body.replace("*name*", d['name'])
        message = message.replace("*domain*", d['domain'])
        subject = head
        email_from = settings.EMAIL_HOST_USER
        recipient = [recipient_list[cnt],]
        print("-----------------------------")
        print(head)
        print(message)
        try:
            x = send_mail(subject, message, email_from, recipient)
            print("$$$$$$$$$$$$$$$$")
            print(x)
        except Exception as e:
            print("!!!!!!!!!!!!>Error In sending Mail to Receipnt")
            print(e)
        print("-----------------------------")

    
        
