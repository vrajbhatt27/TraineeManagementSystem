import os
import shutil
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.core.mail import EmailMessage
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import img2pdf
from fpdf import FPDF


from mainApp.models import Trainee


class PDF(FPDF):
    def header(self):
        self.image(staticfiles_storage.path('logo.jpeg'), 10, 8, 25)
        self.set_font('times', 'B', 24)
        self.ln(10)
        self.cell(80)
        self.cell(30, 12, 'Company Name', border=0, ln=True, align='C')
        self.cell(30, 10, '___________________________________________________________________________________________________',
                  border=0, ln=True, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def offerletter_utility(fid, name='', domain='', to='', all=False):
    path = os.path.join(settings.BASE_DIR, 'media', fid)
    failed_list = []
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
            pdf_path = generateLetter(path, d['name'], d['domain'])
            with open(pdf_path, 'rb') as f:
                pdf_file = f.read()

            res = sendEmailWithAttachment(
                'Regarding Offer Letter', 
                f'Congratulations, you are selected as {d["domain"]} intern. Your offerletter is attached with this mail', 
                d['email'], 
                pdf_file, 
                'offerletter.pdf'
                )
            
            if not res:
                failed_list.append(d['email'])

    else:
        pdf_path = generateLetter(path, name, domain)
        with open(pdf_path, 'rb') as f:
            pdf_file = f.read()
        
        res = sendEmailWithAttachment(
            'Regarding Offer Letter',
            f'Congratulations, you are selected as {domain} intern. Your offerletter is attached with this mail',
            to,
            pdf_file,
            'offerletter.pdf'
        )
        if not res:
            failed_list.append(to)
        
    shutil.rmtree(path)
    return failed_list

def generateLetter(path, name, domain):
    pdf = PDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('helvetica', '', 16)

    pdf.cell(0, 10, f'Dear {name}, ', ln=True)
    pdf.cell(
        0, 10, f'We are glad to offer you the position of {domain} Intern at our Company. ', ln=True)
    pdf.cell(
        0, 10, f'You will be working on projects using {domain}. Lets learn together!', ln=True)
    pdf.cell(20, 10, 'Dummy text........................  ', ln=True)
    pdf.ln(140)
    pdf.cell(20, 10, 'With Regards,  ', ln=True)
    pdf.cell(20, 10, 'Guide name ', ln=True)

    pdf_path = os.path.join(path, '{}.pdf'.format(name))
    pdf.output(pdf_path)
    return pdf_path


def certificate_utility(fid, name='', domain='', to='', all=False):
    path = os.path.join(settings.BASE_DIR, 'media', fid)
    failed_list = []

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
            res = sendEmailWithAttachment('Internship Certificate',
                                    f'The certificate for your {d["domain"]} internship is attached with this mail.', d['email'], pdf, 'certificate.pdf')
            if not res:
                failed_list.append(d['email'])

    else:
        # Generating
        pdf = generateCerti(path, name)

        # sending email
        res = sendEmailWithAttachment('Internship Certificate',
                                      f'The certificate for your {domain} internship is attached with this mail.', to, pdf, 'certificate.pdf')

        if not res:
            failed_list.append(to)
        
    shutil.rmtree(path)
    return failed_list


def sendEmailWithAttachment(subject, body, to, file, file_name):
    res = False
    try:
        email = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [to],
        )

        email.attach(file_name, file, 'application/pdf')
        email.send()
        res = True
    except Exception as e:
        print("Error in sending mail with attachment!!!")
        print(e)

    return res


def generateCerti(path, name):
    url = staticfiles_storage.path('certificate.jpg')
    img_path = os.path.join(path, '{}.jpg'.format(name))

    # generating certi
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

    # Converting to pdf
    img = Image.open(img_path)
    pdf = img2pdf.convert(img.filename)

    img.close()
    return pdf
