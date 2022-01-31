from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .code import newForm

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        if request.POST["newForm"] == "True":
            description = request.POST.get('description')
            domains = request.POST.get('domains')

            res = newForm.setNewForm(description, domains)
            return redirect('home')


    return render(request, 'mainApp/home.html')
