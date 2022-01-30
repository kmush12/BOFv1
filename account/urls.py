from account.views import register_view, login_view,  logout_view, search_view
from django.urls import path

app_name = "account"
urlpatterns = [
        path('login/', login_view, name='login-view'),
        path('logout/', logout_view, name='logout-view'),
        path('register/', register_view, name='register-view'),
        path('search/', search_view, name='search-view'),
    ]