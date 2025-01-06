from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from authapp.api.views import SignUp, LogoutView, ProfileView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view() , name='login'),
    path('signup/', SignUp.as_view() , name='signup'),
    path('logout/', LogoutView.as_view() , name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view() , name='token_refresh'),
    path('profile/', ProfileView.as_view() , name='profile'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
