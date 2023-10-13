from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import ConfirmCode
from .serializer import AuthorizationValidateSerializer, RegistrationValidateSerializer, ConfirmCodeValidateSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        validated['is_active'] = False

        user = User.objects.create_user(**validated)
        return Response(data={'user_id': user.id},
                        status=status.HTTP_201_CREATED)


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = AuthorizationValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_403_FORBIDDEN)


class ConfirmAPIViews(APIView):
    def post(self, request):
        serializer = ConfirmCodeValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if ConfirmCode.objects.filter(code=request.data['code']):
                User.objects.update(is_active=True)
                return Response(status=status.HTTP_202_ACCEPTED)

            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        except ValueError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

