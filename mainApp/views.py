import email
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Form
from .code import newForm, tform_utils


@login_required(login_url='login')
def home(request):
    # print("-------------------")
    # print(request.user.id)
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
            'url': form.fid,
            'form_status': form.form_status,
        })
    return render(request, 'mainApp/home.html', {'forms': mylist})


def tforms(request, fid):
    if request.method == "GET":
        data = tform_utils.getDataForTform(fid)
        if(len(data) == 0):
            return render(request,'mainApp/error.html', {'msg': 'Form Does not Exist'})

        params = {'data': data}
        return render(request, 'mainApp/tform.html', params)
