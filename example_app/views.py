from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from example.serializers import (
    UserSerializer,
    GroupSerializer,
    ProductUserEngagementSerializer,
    ProductSerializer,
)
from example_app.models import Product, ProductUserEngagement


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Product to be viewed or edited.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductUserEngagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ProductUserEngagements to be viewed or edited.
    """

    queryset = ProductUserEngagement.objects.all()
    serializer_class = ProductUserEngagementSerializer
    permission_classes = [permissions.IsAuthenticated]
