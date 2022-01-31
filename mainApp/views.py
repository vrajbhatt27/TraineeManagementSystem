import email
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Form
from .code import newForm


@login_required(login_url='login')
def home(request):
    # print("-------------------")
    # print(request.user.id)
    if request.method == 'POST':
        if request.POST["newForm"] == "True":
            description = request.POST.get('description')
            domains = request.POST.get('domains')
            res = newForm.setNewForm(request.user, description, domains)
            if res:
                return redirect('home')
            else:
                return redirect('mainApp/error.html')

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