import email
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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

    return render(request, 'mainApp/home.html')
