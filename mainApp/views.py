from distutils.command.upload import upload
from turtle import pen
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Form, Test
from .code import newForm, payment_module, tform_utils, tdetails_utils, email_utils, other_utils, test_module
from .code.hashid_utils import encrypt, decrypt
from django.contrib import messages
import csv
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        if request.POST["newForm"] == "True":
            description = request.POST.get('description')
            domains = request.POST.get('domains')
            fee_amount = request.POST.get('payment')
            res = newForm.setBaseForm(
                request.user, description, domains, fee_amount)
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
            'payment_url': encrypt(form.fid),
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


@ login_required(login_url='login')
def toTdetails(request, fid):
    request.session['fid'] = fid
    return HttpResponseRedirect(reverse('tdetails'))


@ login_required(login_url='login')
def tdetails(request):
    tdata = tdetails_utils.getTraineeData(request.session["fid"])
    fdata = tdetails_utils.getFormData(request.session["fid"])
    if len(fdata) == 0:
        return render(request, 'mainApp/error.html', {"msg": "Can't get Trainee Data"})

    return render(request, 'mainApp/traineeDetails.html', {"tdata": tdata, "fdata": fdata})


@ login_required(login_url='login')
def filterTrainee(request):
    if request.method == 'POST':
        score = request.POST.get('score', '')
        payment = request.POST.get('filter_payment')

        if payment:
            tdetails_utils.filterTrainee(request.session['fid'], payment=True)

        if score != '':
            tdetails_utils.filterTrainee(request.session['fid'], score=score)

    return redirect('tdetails')


@ login_required(login_url='login')
def delTrainee(request, temail):
    res = tdetails_utils.delete_trainee(temail, request.session["fid"])
    if not res:
        return render(request, 'mainApp/error.html', {"msg": "Error in Deleting Trainee"})

    return redirect('tdetails')


@ login_required(login_url='login')
def setSession(request, fid):
    request.session['fid_for_utility'] = fid
    return HttpResponse('')


@ login_required(login_url='login')
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


@ login_required(login_url='login')
def urlStatusToogle(request, fid):
    newForm.toogleUrlStatus(fid)
    return HttpResponse('')


@ login_required(login_url='login')
def download_csv(request):
    domain = request.GET.get('domain', '')

    if domain != 'all':
        data = tdetails_utils.getTraineeData(request.session["fid"], domain)
    else:
        data = tdetails_utils.getTraineeData(request.session["fid"])

    if len(data) == 0:
        return render(request, 'mainApp/error.html', {"msg": "No Trainee Present."})

    fields = ['Name', 'Email', 'Age', 'College',
              'CGPA', 'HSC', 'SSC', 'Domain', 'Resume', 'Score', 'Payment']
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
            t['tscore'],
            t['tpaymentStatus'],
        ])

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=data.csv'
    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(fields)
    writer.writerows(rows)

    return response


@ login_required(login_url='login')
def delForm(request, fid):
    res = newForm.deleteForm(fid)
    if not res:
        return render(request, 'mainApp/error.html', {"msg": "Error in Deleting Form"})

    return redirect('home')


@ login_required(login_url='login')
def generateCertificate(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        domain = request.POST.get('domain')
        email = request.POST.get('email')
        file = request.FILES.get('certi')
        send_to_all = request.POST.get('all')

        if name != '':
            res = other_utils.certificate_utility(
                request.session["fid_for_utility"], file, name, domain, email)

            if len(res) == 0:
                messages.success(
                    request, f'Certificate to {name} Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Certificate."})

        if send_to_all != None:
            failed_list = other_utils.certificate_utility(
                request.session["fid_for_utility"], file, all=True)

            if failed_list == -1:
                return render(request, 'mainApp/error.html', {"msg": "Error in retrieving trainee details"})

            if failed_list == -2:
                return render(request, 'mainApp/error.html', {"msg": "Something Went Wrong !!!"})

            if len(failed_list) == 0:
                messages.success(
                    request, 'All Certificates Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Certificates.", "list": failed_list})

    return redirect('home')


@ login_required(login_url='login')
def generateOfferLetter(request):
    if request.method == "POST":
        name = request.POST.get("name")
        domain = request.POST.get('domain')
        email = request.POST.get('email')
        file = request.FILES.get('offer_letter')
        send_to_all = request.POST.get('all')

        if name != '':
            res = other_utils.offerletter_utility(
                request.session["fid_for_utility"], file, name, domain, email)

            if len(res) == 0:
                messages.success(
                    request, f'Offerletter to {name} Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Offerletter."})

        if send_to_all != None:
            failed_list = other_utils.offerletter_utility(
                request.session["fid_for_utility"], file, all=True)

            if failed_list == -1:
                return render(request, 'mainApp/error.html', {"msg": "Error in retrieving trainee details"})

            if len(failed_list) == 0:
                messages.success(
                    request, 'All Offerletters Sent Successfully.')
            else:
                return render(request, 'mainApp/error.html', {"msg": "Error in sending Offerletters.", "list": failed_list})

    return redirect('home')

# Test Module Starts Here


@ login_required(login_url='login')
def createTest(request):
    if request.method == 'POST':
        if request.POST["newTest"] == "True":
            description = request.POST.get('description')
            domain = request.POST.get('domain')
            csv_file = request.POST.get('csv_file')

            if csv_file != '' and domain != '' and description != '':
                myFile = request.FILES.get('csv_file')
                res = test_module.createTest(
                    request.user, description, domain, myFile)

                if not res:
                    return render(request, 'mainApp/error.html', {'msg': 'Something Went Wrong !!!'})

    return redirect('home')


def test_form(request, tid):
    if request.method == "GET":
        data = test_module.getData(tid)
        if(data == -1):
            return render(request, 'mainApp/error.html', {'msg': 'Test is Closed'})

        if(len(data) == 0):
            return render(request, 'mainApp/error.html', {'msg': 'Test Does not Exist'})

        params = {'data': data, 'tid': tid}

    if request.method == "POST":
        email = request.POST.get('email')
        keys = test_module.getKeys(tid)
        ans = []

        for key in keys:
            ans.append(request.POST.get(key))

        res = test_module.saveData(email, ans, tid)

        if res == -1:
            return render(request, 'mainApp/error.html', {"msg": "Test Already Submitted"})

        if res:
            return render(request, 'mainApp/success.html', {"msg": "Test Submitted Successfully"})
        else:
            return render(request, 'mainApp/error.html', {"msg": "Error In Submitting Test !!!"})

    return render(request, 'mainApp/testform.html', params)


@ login_required(login_url='login')
def toogleTestStatus(request, tid):
    test_module.toogleTestStatus(tid)
    return HttpResponse('')


@ login_required(login_url='login')
def delTest(request, tid):
    res = test_module.deleteTest(tid)
    if not res:
        return render(request, 'mainApp/error.html', {"msg": "Error in Deleting Form"})

    return redirect('home')


# Payment Module
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def payment(request, fid):
    if request.method == "GET":
        data = payment_module.getPaymentDetails(fid)
        if(len(data) == 0):
            return render(request, 'mainApp/error.html', {'msg': 'Error in Getting payment details'})

        params = {'data': data}

    return render(request, 'mainApp/payment.html', params)


def makePayment(request):
    if request.method == "POST":
        email = request.POST.get('email')
        fid = request.POST.get('fid')
        data = payment_module.setUpPayment(fid, email, razorpay_client)

        if data == -1:
            return render(request, 'mainApp/error.html', {'msg': 'User Doesn\'t Exist'})

        if data == -2:
            return render(request, 'mainApp/error.html', {'msg': 'Something Went Wrong'})

        params = {'data': data}

    return render(request, 'mainApp/payment.html', params)


@ csrf_exempt
def paymentHandler(request):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)

            if result == True:
                res = payment_module.savePaymentStatus(razorpay_order_id)
                return render(request, 'mainApp/success.html', {"msg": "Payment Successfully"})
            else:
                # if signature verification fails.
                return render(request, 'mainApp/error.html', {"msg": "Payment Failed!!!"})
        except Exception as e:
            return render(request, 'mainApp/error.html', {"msg": "Payment Failed!!!"})

    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
