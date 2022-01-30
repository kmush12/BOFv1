from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, Comment

# Create your views here.
from post.forms import AddPostForm, AddCommentForm


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

def post_like_view(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.likes.all().contains(request.user):
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)
    form = AddCommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.post = post
        new_comment.save()
    context = {
        "post": post,
        "comments": comments,
        "form": form
    }
    return render(request, "post_detail_view.html", context)