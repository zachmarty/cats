from django.urls import reverse
import jwt
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth.hashers import make_password
from users.models import User
from users.serializers import EmailVerificationSerializer, UserSerializer
from users.utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
import rest_framework.status as status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserCreateView(CreateAPIView):
    """Апи создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        if "is_active" in data:
            data["is_active"] = False
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data
        user_email = User.objects.get(email=user["email"])
        tokens = RefreshToken.for_user(user_email).access_token
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(tokens)
        email_body = (
            "Hi "
            + user["username"]
            + " Use the link below to verify your email \n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user["email"],
            "email_subject": "Verify your email",
        }
        Util.send_email(data=data)
        return Response(
            {"user_data": user, "access_token": str(tokens)},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
