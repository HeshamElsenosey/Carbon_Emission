from django.urls import path
from .views import RegisterView, ProfileUpdateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # رابط تسجيل الدخول
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # تجديد التوكن
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
]