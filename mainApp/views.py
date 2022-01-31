from django.shortcuts import render, redirect

from .code import newForm


def home(request):
    if request.method == 'POST':
        if request.POST["newForm"] == "True":
            description = request.POST.get('description')
            domains = request.POST.get('domains')
            
            res = newForm.setNewForm(description, domains)
            return redirect('home')


    return render(request, 'mainApp/home.html')
