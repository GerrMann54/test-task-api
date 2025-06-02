from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.contrib.auth import authenticate

User = get_user_model()  # Импортируем модель пользователя

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Неверные учетные данные.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.email_verified:
            return Response({'error': 'Пожалуйста, подтвердите вашу почту.'}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)


class EmailVerificationView(generics.GenericAPIView):
    def get(self, request, verification_code):
        try:
            user = User.objects.get(verification_code=verification_code)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.email_verified:
            user.email_verified = True
            user.save()
            return Response({'success': 'Email подтвержден!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email уже подтвержден.'}, status=status.HTTP_400_BAD_REQUEST)
