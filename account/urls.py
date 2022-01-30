from account.views import register_view, login_view, logout_view, search_view, requests_list_view, send_request_view, \
        accept_request_view, decline_request_view, profile_view
from django.urls import path

app_name = "account"
urlpatterns = [
        path('login/', login_view, name='login-view'),
        path('logout/', logout_view, name='logout-view'),
        path('register/', register_view, name='register-view'),
        path('search/', search_view, name='search-view'),
        path('requests/', requests_list_view, name='requests-list-view'),
        path('send-request/<int:id>/', send_request_view, name='send-request-view'),
        path('accept-request/<int:id>/', accept_request_view, name='accept-request-view'),
        path('decline-request/<int:id>/', decline_request_view, name='decline-request-view'),
        path('profile/<int:id>', profile_view, name='profile-view'),
    ]