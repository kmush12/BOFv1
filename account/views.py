from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from account.forms import SignUpForm
from account.models import Account
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Account.objects.create(user=user)
        login(request, user)
        return redirect("pages:home-view")
    context = {
        "form": form
    }
    return render(request, "register_view.HTML", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            print()
    form = AuthenticationForm()
    return render(request, "login_view.html", context={"form": form})

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/')
    logout(request)
    return redirect('/')
