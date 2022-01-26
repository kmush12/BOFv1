from django.urls import path

from post.views import home_view

app_name = "post"
urlpatterns = [
        path('', home_view, name='home-view'),
    ]