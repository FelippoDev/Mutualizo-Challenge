
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomRegisterSerializer, CustomUserSerializer, \
    CustomLoginSerializer


class CreateUserView(CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            'user': CustomUserSerializer(instance=user).data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = CustomLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_instance = CustomUserSerializer(instance=user).data['id']
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_200_OK)
