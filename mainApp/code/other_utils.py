import os
import shutil
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.core.mail import EmailMessage
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import img2pdf

from mainApp.models import Trainee


def certificate_utility(fid, name='', domain='', to='', all=False):
    path = os.path.join(settings.BASE_DIR, 'media', fid)
    
    try:
        os.mkdir(path)
    except Exception as e:
        print("Error while creating directory")
        print(e)

    if all:
        data = []
        try:
            trainee_list = Trainee.objects.filter(fid=fid)
            for trainee in trainee_list:
                data.append({
                    'name': trainee.trainee_name,
                    'domain': trainee.trainee_domain,
                    'email': trainee.trainee_email,
                })
        except Exception as e:
            ("!!!!!!!!!!!!>Error In getting data for sending certificate to all")
            print(e)
            return -1

        for d in data:
            pdf = generateCerti(path, d['name'])
            sendEmailWithAttachment('Internship Certificate',
                                    f'The certificate for your {d["domain"]} internship is attached with this mail.', d['email'], pdf)
    else:
        #Generating 
        pdf = generateCerti(path, name)
        
        # sending email
        sendEmailWithAttachment('Internship Certificate',
                                f'The certificate for your {domain} internship is attached with this mail.', to, pdf)

    shutil.rmtree(path)

def sendEmailWithAttachment(subject, body, to, file):
    res = False
    try:
        email = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [to],
        )

        email.attach('certificate.pdf', file, 'application/pdf')
        email.send()
        res = True
    except Exception as e:
        print("Error in sending mail with attachment!!!")
        print(e)

    return res

def generateCerti(path, name):
    url = staticfiles_storage.path('certificate.jpg')
    img_path = os.path.join(path, '{}.jpg'.format(name))

    #generating certi
    font = ImageFont.truetype('arial.ttf', 60)
    font2 = ImageFont.truetype('arial.ttf', 40)

    img = Image.open(url)
    today = datetime.now()
    fdate = today.strftime("%d-%m-%Y")
    draw = ImageDraw.Draw(img)
    draw.text(xy=(725, 760), text=name, fill=(0, 0, 0), font=font)
    draw.text(xy=(300, 1250), text=str(fdate), fill=(0, 0, 0), font=font2)
    img.save(img_path)
    img.close()

    #Converting to pdf
    img = Image.open(img_path)
    pdf = img2pdf.convert(img.filename)

    img.close()
    return pdf
