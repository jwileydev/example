from django.contrib.auth.models import User, Group
from rest_framework import serializers
from example_app.models import Product, ProductUserEngagement


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class ProductUserEngagementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductUserEngagement
        fields = ["url", "product", "user", "engagement", "created"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ["url", "name", "description", "likes", "dislikes", "created"]
        engagements = ProductUserEngagementSerializer(many=True, read_only=True)
