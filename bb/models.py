from django.db import models
from django.conf import settings
from django.utils import timezone
from unidecode import unidecode
from django.template import defaultfilters
from uuslug import slugify # преобразование заголовков в ссылки pip install django-uuslug

class PostProduct(models.Model):
    title = models.CharField(max_length=210)# название товара
    translit_title = models.CharField(verbose_name='Транслит', max_length=210, blank=True)  # сохранение ссылки
    text = models.TextField()# описание товара
    price = models.IntegerField(default=0)# цена товара
    first_appearance_date = models.DateTimeField(default=timezone.now)# первая публикация товара
    image = models.ImageField(null=True, blank=True, upload_to='images/products')# фото товара
    seo_keywords = models.CharField('Keywords', blank=True, max_length=250)

    def publish(self):
        self.first_appearance_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def save(self):
        self.translit_title = '{0}-{1}'.format('be-better', defaultfilters.slugify(unidecode(self.title)))# slugify(self.title)
        super(PostProduct, self).save()

# Create your models here.
