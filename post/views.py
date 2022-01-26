from django.shortcuts import render, redirect
from post.models import Post

# Create your views here.

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    friends = request.user.account.friends.all()
    queryset = Post.objects.all().order_by('-date')
    context = {
        "queryset": queryset,
        "friends": friends
    }
    return render(request, "home_view.html", context)