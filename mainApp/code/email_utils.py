import csv
from ctypes import resize
from django.conf import settings
from django.core.mail import send_mail
from ..models import Trainee


def sendToReceipnt(to, head, body):
    subject = head
    message = body
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to, ]
    res = False
    try:
        send_mail(subject, message, email_from, recipient_list)
        res = True
    except Exception as e:
        print("!!!!!!!!!!!!>Error In sending Mail to Receipnt")
        print(e)

    return res


def sendToAll(head, body, fid):
    data = []
    failed_list = []
    try:
        trainee_list = Trainee.objects.filter(fid=fid)
        for trainee in trainee_list:
            data.append({
                'name': trainee.trainee_name,
                'domain': trainee.trainee_domain,
                'email': trainee.trainee_email,
            })
    except Exception as e:
        print("!!!!!!!!!!!!>Error In getting data for sending email to all")
        print(e)
        return -1

    for d in data:
        message = ''
        message = body.replace("*name*", d['name'])
        message = message.replace("*domain*", d['domain'])
        subject = head
        email_from = settings.EMAIL_HOST_USER
        recipient = [d['email'], ]
        try:
            send_mail(subject, message, email_from, recipient)
        except Exception as e:
            print("!!!!!!!!!!!!>Error In sending Mail to Receipnt")
            print(e)
            failed_list.append(d['email'])

    return failed_list


def sendToFile(file, head, body):
    file = file.read().decode().splitlines()
    reader = csv.reader(file)
    data = []
    failed_list = []
    for row in reader:
        data.append({
            'name': row[0],
            'email': row[1],
            'domain': row[2],
        })

    for d in data:
        message = ''
        message = body.replace("*name*", d['name'])
        message = message.replace("*domain*", d['domain'])
        subject = head
        email_from = settings.EMAIL_HOST_USER
        recipient = [d['email'], ]
        try:
            send_mail(subject, message, email_from, recipient)
        except Exception as e:
            print("!!!!!!!!!!!!>Error In sending Mail to Receipnt")
            print(e)
            failed_list.append(d['email'])

    return failed_list
