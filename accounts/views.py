from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, get_user_model

from .serializers import RegisterUserSerializer
from .permissions import AnonUsersOnly

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_payload_encoder = api_settings.JWT_ENCODE_HANDLER
jwt_payload_response_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


# Create your views here.

class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already logged in'})
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        payload = jwt_payload_handler(user)
        token = jwt_payload_encoder(payload)
        response = jwt_payload_response_handler(token, user, request=request)
        return Response(response)


class RegisterApiView(generics.CreateAPIView):
    permission_classes = [AnonUsersOnly]
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    # def get_serializer_context(self, *args, **kwargs):
    #     return {'request': self.request}
