from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
)


def serialize_user(user, request):
    return UserProfileSerializer(user, context={'request': request}).data


class UserRegistrationView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        return render(request, 'users/register.html')


class UserLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'users/login.html', {'error': 'Login failed.'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return render(request, 'users/profile.html', {'user': request.user})


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(serialize_user(request.user, request))

    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated.',
                'user': serialize_user(request.user, request),
            })
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'success': True,
            'message': 'Registered.',
            'user': serialize_user(user, request),
        }, status=status.HTTP_201_CREATED)
    return Response(
        {'success': False, 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {'success': False, 'message': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    login(request, user)
    token, _created = Token.objects.get_or_create(user=user)
    return Response({
        'success': True,
        'message': 'Logged in.',
        'user': serialize_user(user, request),
        'token': token.key,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return Response({'success': True, 'message': 'Logged out.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    return Response(serialize_user(request.user, request))
