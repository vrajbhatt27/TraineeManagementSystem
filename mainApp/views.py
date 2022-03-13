from distutils.command.upload import upload
from turtle import pen
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Form, Test
from .code import newForm, tform_utils, tdetails_utils, email_utils, other_utils, test_module
from .code.hashid_utils import encrypt, decrypt
from django.contrib import messages
import csv


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        if request.POST["newForm"] == "True":
            description = request.POST.get('description')
            domains = request.POST.get('domains')
            res = newForm.setBaseForm(request.user, description, domains)
            if res:
                return redirect('home')
            else:
                return render(request, 'mainApp/error.html', {'msg': 'Something Went Wrong !!!'})

    formList = Form.objects.filter(uid=request.user)
    mylist = []
    for form in formList:
        mylist.append({
            'date': form.date,
            'description': form.description,
            'url': encrypt(form.fid),
            'form_status': form.form_status,
            'fid': form.fid,
        })

    testList = Test.objects.filter(uid=request.user)
    mylist2 = []
    for cnt, test in enumerate(testList, 1):
        mylist2.append({
            'cnt': cnt,
            'domain': test.domain,
            'url': encrypt(test.test_id),
            'test_status': test.test_status,
            'tid': test.test_id,
        })
    return render(request, 'mainApp/home.html', {'forms': mylist, 'tests': mylist2})

# ------------------------------


@login_required(login_url='login')
def createTest(request):
    if request.method == 'POST':
        if request.POST["newTest"] == "True":
            description = request.POST.get('description')
            domain = request.POST.get('domain')
            csv_file = request.POST.get('csv_file')

            if csv_file != '':
                myFile = request.FILES.get('csv_file')
                test_module.createTest(
                    request.user, description, domain, myFile)

    return redirect('home')
# ------------------------------


def tforms(request, fid):
    if request.method == "GET":
        data = tform_utils.getDataForTform(fid)
        if(data == -1):
            return render(request, 'mainApp/error.html', {'msg': 'Form is Closed'})

        if(len(data) == 0):
            return render(request, 'mainApp/error.html', {'msg': 'Form Does not Exist'})

        params = {'data': data}

    if request.method == "POST":
        res = tform_utils.saveDataForTform(
            fid,
            request.POST.get("name"),
            request.POST.get("email"),
            request.POST.get("age"),
            request.POST.get("college"),
            request.POST.get("cgpa"),
            request.POST.get("hsc"),
            request.POST.get("ssc"),
            request.POST.get("domain"),
            request.POST.get("resume"),
        )
        if res == -1:
            return render(request, 'mainApp/error.html', {"msg": "Form Already Submitted"})

        if res:
            return render(request, 'mainApp/success.html', {"msg": "Form Submitted Successfully"})
        else:
            return render(request, 'mainApp/error.html', {"msg": "Error In Submitting Form !!!"})

    return render(request, 'mainApp/tform.html', params)


@login_required(login_url='login')
def toTdetails(request, fid):
    request.session['fid'] = fid
    return HttpResponseRedirect(reverse('tdetails'))


@login_required(login_url='login')
def tdetails(request):
    tdata = tdetails_utils.getTraineeData(request.session["fid"])
    fdata = tdetails_utils.getFormData(request.session["fid"])
    if len(fdata) == 0:
        return render(request, 'mainApp/error.html', {"msg": "Can't get Trainee Data"})

    return render(request, 'mainApp/traineeDetails.html', {"tdata": tdata, "fdata": fdata})


@login_required(login_url='login')
def delTrainee(request, temail):
    res = tdetails_utils.delete_trainee(temail, request.session["fid"])
    if not res:
        return render(request, 'mainApp/error.html', {"msg": "Error in Deleting Trainee"})

    return redirect('tdetails')


@login_required(login_url='login')
def setSession(request, fid):
    request.session['fid_for_utility'] = fid
    return HttpResponse('')


@login_required(login_url='login')
def sendEmail(request):
    if request.method == 'POST':
        email_head = request.POST.get('email_heading')
        email_body = request.POST.get('email_body')
        receipnt = request.POST.get('receipnt')
        csv_file = request.POST.get('csv_file')
        send_to_all = request.POST.get('all')

        if receipnt != '':
            res = email_utils.sendToReceipnt(receipnt, email_head, email_body)
            if res:
                messages.success(
                    request, f'Email to {receipnt} Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Email."})

        if csv_file != '':
            myFile = request.FILES.get('csv_file')
            failed_list = email_utils.sendToFile(
                myFile, email_head, email_body)
            if len(failed_list) == 0:
                messages.success(
                    request, 'All Emails Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Email.",
                                                              "list": failed_list})

        if send_to_all != None:
            failed_list = email_utils.sendToAll(email_head, email_body,
                                                request.session['fid_for_utility'])

            if failed_list == -1:
                return render(request, 'mainApp/error.html', {"msg": "Error in retrieving trainee details"})

            if len(failed_list) == 0:
                messages.success(
                    request, 'All Emails Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Email.",
                                                              "list": failed_list})

    return redirect('home')


@login_required(login_url='login')
def urlStatusToogle(request, fid):
    newForm.toogleUrlStatus(fid)
    return HttpResponse('')


@login_required(login_url='login')
def download_csv(request):
    data = tdetails_utils.getTraineeData(request.session["fid"])

    if len(data) == 0:
        return render(request, 'mainApp/error.html', {"msg": "No Trainee Present."})

    fields = ['Name', 'Email', 'Age', 'College',
              'CGPA', 'HSC', 'SSC', 'Domain', 'Resume']
    rows = []

    for t in data:
        rows.append([
            t['tname'],
            t['temail'],
            t['tage'],
            t['tcollege'],
            t['tcgpa'],
            t['thsc'],
            t['tssc'],
            t['tdomain'],
            t['tresume'],
        ])

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=data.csv'
    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(fields)
    writer.writerows(rows)

    return response


@login_required(login_url='login')
def delForm(request, fid):
    res = newForm.deleteForm(fid)
    if not res:
        return render(request, 'mainApp/error.html', {"msg": "Error in Deleting Form"})

    return redirect('home')


@login_required(login_url='login')
def generateCertificate(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        domain = request.POST.get('domain')
        email = request.POST.get('email')
        send_to_all = request.POST.get('all')

        if name != '':
            res = other_utils.certificate_utility(
                request.session["fid_for_utility"], name, domain, email)

            if len(res) == 0:
                messages.success(
                    request, f'Certificate to {name} Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Certificate."})

        if send_to_all != None:
            failed_list = other_utils.certificate_utility(
                request.session["fid_for_utility"], all=True)

            if failed_list == -1:
                return render(request, 'mainApp/error.html', {"msg": "Error in retrieving trainee details"})

            if len(failed_list) == 0:
                messages.success(
                    request, 'All Certificates Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Certificates.", "list": failed_list})

    return redirect('home')


@login_required(login_url='login')
def generateOfferLetter(request):
    if request.method == "POST":
        cname = request.POST.get("cname")
        hr = request.POST.get('hrName')
        name = request.POST.get("name")
        domain = request.POST.get('domain')
        email = request.POST.get('email')
        send_to_all = request.POST.get('all')

        if name != '':
            res = other_utils.offerletter_utility(
                request.session["fid_for_utility"], cname, hr, name, domain, email)

            if len(res) == 0:
                messages.success(
                    request, f'Offerletter to {name} Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Offerletter."})

        if send_to_all != None:
            failed_list = other_utils.offerletter_utility(
                request.session["fid_for_utility"], cname, hr, all=True)

            if failed_list == -1:
                return render(request, 'mainApp/error.html', {"msg": "Error in retrieving trainee details"})

            if len(failed_list) == 0:
                messages.success(
                    request, 'All Offerletters Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Offerletters.", "list": failed_list})

    return redirect('home')

# Test Module Starts Here
