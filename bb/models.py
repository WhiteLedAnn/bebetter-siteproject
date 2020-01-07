from django.db import models
from django.conf import settings
from django.utils import timezone
from unidecode import unidecode # pip install unidecode
from django.template import defaultfilters
from uuslug import slugify # преобразование заголовков в ссылки pip install django-uuslug
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PostProduct(models.Model):
    title = models.CharField(max_length=210)# название товара
    translit_title = models.CharField(verbose_name='Транслит', max_length=210, blank=True)# сохранение ссылки
    text = models.TextField()# описание товара
    price = models.IntegerField(default=0)# цена товара на сайте - стоимость продажи
    in_stock = models.BooleanField(default=True)# в наличии на складе (ИЗМЕНИТЬ - по умолчанию товара нет) 
    published = models.BooleanField(default=False)# публикация на сайте по умолчанию товар не опубликован
    last_update_date = models.DateTimeField(default=timezone.now)# последнее обновление информации о товаре
    image = models.ImageField(null=True, blank=True, upload_to='images/products')# фото товара
    seo_keywords = models.CharField('Keywords', blank=True, max_length=250)

    def publish(self):
        self.first_appearance_date = timezone.now()
        self.published = True
        self.save()

    def __str__(self):
        return self.title

    def save(self):
        self.translit_title = '{0}-{1}'.format('be-better', defaultfilters.slugify(unidecode(self.title)))# slugify(self.title)
        super(PostProduct, self).save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# Create your models here.
