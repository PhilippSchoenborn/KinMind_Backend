# Drittanbieter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model

# Lokale Importe
from .serializers import RegistrationSerializer, UserSerializer

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    """API endpoint for user registration."""
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new user and return a token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'fullname': user.fullname,
            'email': user.email,
            'user_id': user.id
        }
        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """API endpoint for user login."""
    def post(self, request):
        """Authenticate user and return a token."""
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'fullname': user.fullname,
                'email': user.email,
                'user_id': user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class EmailCheckView(APIView):
    """API endpoint to check if an email exists."""
    def get(self, request):
        """Return user data if email exists, else 404."""
        email = request.query_params.get('email')
        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            data = UserSerializer(user).data
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)
