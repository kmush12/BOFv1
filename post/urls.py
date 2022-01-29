from django.urls import path

from post.views import home_view, post_create_view

app_name = "post"
urlpatterns = [
        path('', home_view, name='home-view'),
        path('post-create/', post_create_view, name='post-create-view'),
    ]