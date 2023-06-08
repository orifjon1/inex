from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics, permissions, filters

from .serializer import UserSignUpSerializer, SectorSerializer, \
                        RefreshTokenSerializer, UserProfileSerializer, UserStatSerializer
from .models import CustomUser, Sector
from api import permission


class SignUpView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [permission.IsDirector]


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response({"detail": "Logout successful."})


class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer


class RequestUserProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        else:
            return Response(
                serializer.errors
            )


class SectorEmployeeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, id):
        sector = Sector.objects.get(id=id)
        users = CustomUser.objects.filter(Q(status='employee') & Q(sector=sector))
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)


class RequestUserStatView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        serializer = UserStatSerializer(user)
        return Response(serializer.data)


class UserProfileListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = CustomUser.objects.filter(Q(status='manager') | Q(status='employee'))
    serializer_class = UserProfileSerializer


class UserStatListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().exclude(status='director').exclude(status='admin')
    serializer_class = UserStatSerializer


class ManagerStatListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = CustomUser.objects.filter(status='manager')
    serializer_class = UserStatSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']


class EmployeeStatListView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = CustomUser.objects.filter(status='employee')
    serializer_class = UserStatSerializer


class SectorCreateListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permission.IsDirector]
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class SectorDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permission.IsDirector]
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

