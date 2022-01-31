from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, Comment
from post.forms import AddPostForm, AddCommentForm
from BOF.settings import LOGS_ROOT
import os

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
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n Utworzono post")
        f.close()
        form = AddPostForm()
    context = {
        "form": form
    }
    return render(request, "post_create_view.html", context)

def post_like_view(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.likes.all().contains(request.user):
        post.likes.add(request.user)
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n Polubiono posta")
        f.close()
    else:
        post.likes.remove(request.user)
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n Odlubiono posta")
        f.close()
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
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n Dodano komentarz")
        f.close()
    context = {
        "post": post,
        "comments": comments,
        "form": form
    }
    return render(request, "post_detail_view.html", context)