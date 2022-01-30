from django.urls import path

from post.views import home_view, post_create_view, post_like_view, post_detail_view

app_name = "post"
urlpatterns = [
        path('', home_view, name='home-view'),
        path('post-create/', post_create_view, name='post-create-view'),
        path('post-like/<int:id>', post_like_view, name='post-like-view'),
        path('post/<int:id>', post_detail_view, name='post-detail-view'),
    ]