from django.shortcuts import render, redirect
from post.models import Post

# Create your views here.
from post.forms import AddPostForm


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

def post_create_view(request):
    form = AddPostForm(request.POST or None, request.FILES)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.save()
        form = AddPostForm()
    context = {
        "form": form
    }
    return render(request, "post_create_view.html", context)