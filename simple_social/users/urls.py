from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView

from .views import RegisterView


auth_patterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('registration/', RegisterView.as_view(), name='registration'),
]
