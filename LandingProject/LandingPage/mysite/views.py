from django.shortcuts import render
from django.http import HttpResponse
from mysite.models import Info


def index(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        s = Info(firstname = fname,lastname = lname,username = uname, email = email,password = password,)
        s.save()
      #  c = Info.objects.count()
      #  print(c)
    return render(request, 'mysite/index.html')


