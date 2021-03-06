from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from locations.models import Provider
from locations.serializers import (
    LoginSerializer,
    ProviderSerializer,
    RegisterSerializer,
)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action


# Create your views here.
class ProvidersView(ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = ProviderSerializer

    def list(self, request, *args, **kwargs):
        try:
            data = Provider.objects.all()
            serializer = self.serializer_class(data, many=True)
            return Response(
                {"message": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, *args, **kwargs):
        provider = get_object_or_404(Provider, id=pk)
        serializer = self.serializer_class(provider)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        provider = get_object_or_404(Provider, id=pk)
        serializer = self.serializer_class(provider, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": f"successully updated details for the Provider: {serializer.data.get('username')}",
                    "data": serializer.data,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk, *args, **kwargs):
        provider = get_object_or_404(Provider, id=pk)
        name = provider.username
        provider.delete()
        return Response(
            {"message": f"{name} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                Provider,
                username=serializer.validated_data["username"],
            )
            if user.check_password(serializer.validated_data["password"]):
                login(request, user)
                token = str(Token.objects.get_or_create(user=user)[0])
                return Response(
                    {"success": "User has been logged in", "token": token},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": f"password incorrect"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        try:
            logout(request)
            return Response({"success": "Logout Complete"}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {
                    "error": f"The following error occurred while trying to log you out. {str(err)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["POST"])
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"message": "success", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as error:
                return Response(
                    {"error": str(error)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
