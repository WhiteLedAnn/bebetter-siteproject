from django.db import models
from django.conf import settings
from django.utils import timezone

class PostProduct(models.Model):
    title = models.CharField(max_length=210)# название товара
    text = models.TextField()# описание товара
    price = models.IntegerField(default=0)# цена товара
    first_appearance_date = models.DateTimeField(default=timezone.now)# первая публикация товара
    image = models.ImageField(null=True, blank=True, upload_to='images/products')# фото товара

    def publish(self):
        self.first_appearance_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
# Create your models here.
