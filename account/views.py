from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from account.forms import SignUpForm
from account.models import Account, Request
from django.db.models import Q
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
    return redirect('post:home-view')

def decline_request_view(request, id):
    requesto = get_object_or_404(Request, id=id)
    requesto.delete()
    return redirect('post:home-view')