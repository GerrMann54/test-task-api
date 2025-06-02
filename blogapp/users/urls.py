from django.urls import path
from .views import *

urlpatterns = [
    path('reg/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify-email/<uuid:verification_code>/', EmailVerificationView.as_view(), name='email-verify'),
]
