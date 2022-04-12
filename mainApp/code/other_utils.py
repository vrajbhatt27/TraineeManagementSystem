import os
import shutil
from django.conf import settings
from django.core.mail import EmailMessage
from docx import Document

from mainApp.models import Trainee


# Offerletter Utility


def offerletter_utility(fid, file, name='', domain='', to='', all=False):
    path = os.path.join(settings.BASE_DIR, 'media', fid)
    failed_list = []

    # Making Folder

    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print("Error while creating directory")
        print(e)

    # Saving Uploaded file

    try:
        with open(os.path.join(path, 'offer_letter.docx'), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except:
        print(e)
        return -2

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
            pdf_path = generateDoc(
                path, d['name'], d['domain'], 'offer_letter')
            with open(pdf_path, 'rb') as f:
                pdf_file = f.read()

            res = sendEmailWithAttachment(
                'Regarding Offer Letter',
                f'Congratulations, you are selected as {d["domain"]} intern. Your offer letter is attached with this mail',
                d['email'],
                pdf_file,
                'offerletter.docx'
            )

            if not res:
                failed_list.append(d['email'])

    else:
        pdf_path = generateDoc(path, name, domain, 'offer_letter')
        with open(pdf_path, 'rb') as f:
            pdf_file = f.read()

        res = sendEmailWithAttachment(
            'Regarding Offer Letter',
            f'Congratulations, you are selected as {domain} intern. Your offer letter is attached with this mail',
            to,
            pdf_file,
            'offerletter.docx'
        )
        if not res:
            failed_list.append(to)

    shutil.rmtree(path)
    return failed_list


# Certificate Utility


def certificate_utility(fid, file, name='', domain='', to='', all=False):
    path = os.path.join(settings.BASE_DIR, 'media', fid)
    failed_list = []

    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print("Error while creating directory")
        print(e)

    # Saving Uploaded file

    try:
        with open(os.path.join(path, 'certi.docx'), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except:
        print(e)
        return -2

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
            print(
                "!!!!!!!!!!!!>Error In getting data for sending certificate to all")
            print(e)
            return -1

        for d in data:
            doc_path = generateDoc(path, d['name'], d['domain'], 'certi')

            with open(doc_path, 'rb') as f:
                doc = f.read()

            res = sendEmailWithAttachment('Internship Certificate',
                                          f'The certificate for your {d["domain"]} internship is attached with this mail.', d['email'], doc, 'certificate.docx')
            if not res:
                failed_list.append(d['email'])
    else:
        # Generating
        doc_path = generateDoc(path, name, domain, 'certi')

        with open(doc_path, 'rb') as f:
            doc = f.read()
        # sending email
        res = sendEmailWithAttachment('Internship Certificate',
                                      f'The certificate for your {domain} internship is attached with this mail.', to, doc, 'certificate.docx')

        if not res:
            failed_list.append(to)

    shutil.rmtree(path)
    return failed_list


def generateDoc(path, name, domain, file_name):
    document = Document(os.path.join(path, f'{file_name}.docx'))

    # print(document)
    for p in document.paragraphs:
        if '*name*' in p.text or '*domain*' in p.text:
            para = p.text
            para = para.replace('*name*', name)
            para = para.replace('*domain*', domain)
            p.text = para

    document.save(os.path.join(path, f'{name}.docx'))
    return os.path.join(path, f'{name}.docx')

# Send Email with attachment.


def sendEmailWithAttachment(subject, body, to, file, file_name):
    res = False
    try:
        email = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [to],
        )

        email.attach(
            file_name, file, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        email.send()
        res = True
    except Exception as e:
        print("Error in sending mail with attachment!!!")
        print(e)

    return res
