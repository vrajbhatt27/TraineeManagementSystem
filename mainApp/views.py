from turtle import pen
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Form
from .code import newForm, tform_utils, tdetails_utils, email_utils
from .code.hashid_utils import encrypt, decrypt


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
                return redirect('mainApp/error.html', {'msg': 'Something Went Wrong !!!'})

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
    return render(request, 'mainApp/home.html', {'forms': mylist})


def tforms(request, fid):
    if request.method == "GET":
        data = tform_utils.getDataForTform(fid)
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
    print(".............................")
    print(request.session['fid_for_utility'])
    print(".............................")
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
            email_utils.sendToReceipnt(receipnt, email_head, email_body)
            print("Done")

        if csv_file != '':
            print("--------------------------------")
            print(csv_file)
            print("--------------------------------")

        if send_to_all != None:
            email_utils.sendToAll(email_head, email_body,
                                  request.session['fid_for_utility'])
    return redirect('home')
