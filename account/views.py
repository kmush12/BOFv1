from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from account.forms import SignUpForm, UpdateFirstNameForm, UpdateLastNameForm, UpdateImageForm
from account.models import Account, Request
from django.db.models import Q
from post.models import Post
from BOF.settings import LOGS_ROOT
import os

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Account.objects.create(user=user)
        login(request, user)
        f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
        f.write("\n Stworzono nowe konto")
        f.close()
        return redirect("post:home-view")
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
                f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
                f.write("\n Zalogowano uzytkownika")
                f.close()
                return redirect('/')
        else:
            print()
    form = AuthenticationForm()
    return render(request, "login_view.html", context={"form": form})

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/')
    f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
    f.write("\n Wylogowano")
    f.close()
    logout(request)
    return redirect('/')

def search_view(request, *args, **kwargs):
    query = request.GET.get('query')
    users_list = User.objects.filter(
        (Q(first_name__icontains=query) | Q(last_name__icontains=query))
    )
    context = {
        "queryset": users_list
    }
    return render(request, "search_view.html", context)
    
def send_request_view(request, id):
    user = get_object_or_404(User, id=id)
    if not user in request.user.account.friends.all():
        try:
            requesto = Request.objects.get(user_from=request.user, user_to=user)
        except Request.DoesNotExist:
            requesto = None
        if not requesto:
            Request.objects.create(user_from=request.user, user_to=user)
            f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
            f.write("\n Zaproszono uzytkownika")
            f.close()
    return redirect('post:home-view')

def requests_list_view(request):
    requests = Request.objects.filter(user_to=request.user)
    context = {
        'requests': requests
    }
    return render(request, "requests_list_view.html", context)

def accept_request_view(request, id):
    requesto = get_object_or_404(Request, id=id)
    request.user.account.friends.add(requesto.user_from)
    requesto.user_from.account.friends.add(request.user)
    requesto.delete()
    f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
    f.write("\n Zaakcpeptowano prosbe")
    f.close()
    return redirect('post:home-view')

def decline_request_view(request, id):
    requesto = get_object_or_404(Request, id=id)
    requesto.delete()
    f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
    f.write("\n Odrzucono prosbe")
    f.close()
    return redirect('post:home-view')

def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(user=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, "profile_view.html", context)

def settings_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/')
    form1 = UpdateFirstNameForm(request.POST or None, instance=request.user)
    form2 = UpdateLastNameForm(request.POST or None, instance=request.user)
    form3 = UpdateImageForm(request.POST or None, request.FILES, instance=get_object_or_404(Account, user=request.user))
    if 'update_first_name' in request.POST:
        if form1.is_valid():
            form1.save()
            f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
            f.write("\n Zmieniono imie")
            f.close()
            return redirect('account:settings-view')
    elif 'update_last_name' in request.POST:
        if form2.is_valid():
            form2.save()
            f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
            f.write("\n Zmieniono nazwisko")
            f.close()
            return redirect('account:settings-view')
    elif 'update_image' in request.POST:
        if form3.is_valid():
            form3.save()
            f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
            f.write("\n Zmieniono zdjecie")
            f.close()
            return redirect('account:settings-view')
    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3
    }
    return render(request, "settings_view.html", context)