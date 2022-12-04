from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from .models import Product, ProductUserEngagement, EngagementType
from .views import ProductUserEngagementViewSet
import json


class SimpleTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.users = [
            User.objects.create_user(
                username="test0", email="test0@test.com", password="secret0"
            ),
            User.objects.create_user(
                username="test1", email="test1@test.com", password="secret1"
            ),
            User.objects.create_user(
                username="test2", email="test2@test.com", password="secret2"
            ),
        ]
        self.products = [
            Product.objects.create(name="test1", description="desc1"),
            Product.objects.create(name="test2", description="desc2"),
            Product.objects.create(name="test3", description="desc3"),
            Product.objects.create(name="test4", description="desc4"),
        ]


class TestProductUserEngagement(SimpleTest):
    def test_product_user_engagement_dislike_product(self):
        product = Product.objects.create(name="test", description="desc")
        ProductUserEngagement.objects.create(
            user=self.users[0], product=product, engagement=EngagementType.DISLIKE
        )
        product_engagement = ProductUserEngagement.objects.filter(
            engagement=EngagementType.DISLIKE
        )
        self.assertEquals(len(product_engagement), 1)
        self.assertEquals(product_engagement[0].engagement, EngagementType.DISLIKE)

    def test_product_user_engagement_like_product(self):
        product = Product.objects.create(name="test", description="desc")
        ProductUserEngagement.objects.create(
            user=self.users[0], product=product, engagement=EngagementType.LIKE
        )
        product_engagement = ProductUserEngagement.objects.filter(
            engagement=EngagementType.LIKE
        )
        self.assertEquals(len(product_engagement), 1)
        self.assertEquals(product_engagement[0].engagement, EngagementType.LIKE)

    def test_product_user_engagement_multiple_products(self):
        ProductUserEngagement.objects.create(
            user=self.users[0], product=self.products[0], engagement=EngagementType.LIKE
        )
        ProductUserEngagement.objects.create(
            user=self.users[0], product=self.products[1], engagement=EngagementType.LIKE
        )
        ProductUserEngagement.objects.create(
            user=self.users[0],
            product=self.products[2],
            engagement=EngagementType.DISLIKE,
        )
        ProductUserEngagement.objects.create(
            user=self.users[0],
            product=self.products[3],
            engagement=EngagementType.DISLIKE,
        )
        liked_products = [self.products[0], self.products[1]]
        disliked_products = [self.products[2], self.products[3]]
        product_likes = ProductUserEngagement.objects.filter(
            engagement=EngagementType.LIKE
        )
        self.assertEquals(len(product_likes), len(liked_products))
        product_dislikes = ProductUserEngagement.objects.filter(
            engagement=EngagementType.DISLIKE
        )
        self.assertEquals(len(product_dislikes), len(disliked_products))

    def test_product_user_engagement_multiple_engagements(self):
        product = Product.objects.create(name="test1", description="desc1")
        ProductUserEngagement.objects.create(
            user=self.users[0], product=product, engagement=EngagementType.LIKE
        )
        ProductUserEngagement.objects.create(
            user=self.users[1], product=product, engagement=EngagementType.DISLIKE
        )
        liked_products = [product]
        disliked_products = [product]
        product_likes = ProductUserEngagement.objects.filter(
            engagement=EngagementType.LIKE
        )
        self.assertEquals(len(product_likes), len(liked_products))
        product_dislikes = ProductUserEngagement.objects.filter(
            engagement=EngagementType.DISLIKE
        )
        self.assertEquals(len(product_dislikes), len(disliked_products))

    def test_product_likes_multiple_engagements(self):
        product = Product.objects.create(name="test1", description="desc1")
        ProductUserEngagement.objects.create(
            user=self.users[0], product=product, engagement=EngagementType.LIKE
        )
        ProductUserEngagement.objects.create(
            user=self.users[1], product=product, engagement=EngagementType.LIKE
        )
        ProductUserEngagement.objects.create(
            user=self.users[2], product=product, engagement=EngagementType.DISLIKE
        )
        liked_products = [product, product]
        disliked_products = [product]
        self.assertEquals(len(liked_products), product.likes)
        self.assertEquals(len(disliked_products), product.dislikes)


class TestEngagementsAPI(SimpleTest):
    def test_engagements_api(self):
        # using the engagements API, create several product engagements from multiple users
        url = "/engagements/"
        likes = 0
        dislikes = 0
        self.client.force_authenticate(user=self.users[0])
        response = self.client.post(
            url,
            {
                "product": f"/products/{self.products[0].pk}/",
                "user": f"/users/{self.users[0].pk}/",
                "engagement": EngagementType.LIKE,
            },
        )
        self.assertTrue(status.is_success(response.status_code))
        likes += 1
        self.client.force_authenticate(user=self.users[1])
        response = self.client.post(
            url,
            {
                "product": f"/products/{self.products[0].pk}/",
                "user": f"/users/{self.users[1].pk}/",
                "engagement": EngagementType.DISLIKE,
            },
        )
        self.assertTrue(status.is_success(response.status_code))
        dislikes += 1
        self.client.force_authenticate(user=self.users[2])
        response = self.client.post(
            url,
            {
                "product": f"/products/{self.products[0].pk}/",
                "user": f"/users/{self.users[2].pk}/",
                "engagement": EngagementType.DISLIKE,
            },
        )
        self.assertTrue(status.is_success(response.status_code))
        engagement = ProductUserEngagement.objects.last()
        dislikes += 1
        product_detail_url = f"/products/{self.products[0].pk}/"
        response = self.client.get(product_detail_url)
        self.assertTrue(status.is_success(response.status_code))
        product = Product.objects.get(pk=self.products[0].pk)
        self.assertEquals(product.likes, likes)
        self.assertEquals(product.dislikes, dislikes)
        # change dislike to like
        response = self.client.patch(
            f"/engagements/{engagement.pk}/",
            {"engagement": EngagementType.LIKE},
        )
        self.assertTrue(status.is_success(response.status_code))
        dislikes -= 1
        likes += 1
        # Get the product from the API
        response = self.client.get(product_detail_url)
        self.assertTrue(status.is_success(response.status_code))
        product = Product.objects.get(pk=self.products[0].pk)
        self.assertEquals(product.likes, likes)
        self.assertEquals(product.dislikes, dislikes)
