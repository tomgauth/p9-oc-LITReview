from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('feed')
    else:
        return render(request, 'home.html', {'error_message':'invalid login'})
