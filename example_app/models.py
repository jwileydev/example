from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

User = get_user_model()
EngagementType = models.TextChoices("EngagementType", "LIKE DISLIKE")


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def likes(self):
        return Product.objects.filter(
            id=self.pk, productuserengagement__engagement=EngagementType.LIKE
        ).count()

    @property
    def dislikes(self):
        return Product.objects.filter(
            id=self.pk, productuserengagement__engagement=EngagementType.DISLIKE
        ).count()


class ProductUserEngagement(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    engagement = models.CharField(max_length=8, choices=EngagementType.choices)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"], name="unique_user_product"
            )
        ]

        indexes = [
            models.Index(fields=["user", "product"]),
            models.Index(fields=["product", "engagement"]),
        ]
