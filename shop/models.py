import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def get_absolute_url(self):
        return reverse('shop:products_by_category', args=[self.id])

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    count_sold = models.IntegerField(default=0, blank=True, null=True)
    slug = models.SlugField(null=True, unique=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100,200)],
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        ordering = ('-count_sold',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_absolute_url(self):
        return reverse('shop:prod_details', args=[self.category.id, self.id])

    def __str__(self):
        return self.name

class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='review',

    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=140)
    photo = models.ImageField(upload_to='photo/', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    approved_review = models.BooleanField(default=False)
    

    def approve(self):
        self.approved_review = True
        self.save()
    
    class Meta:
        ordering = ['-created_date',] 

    def __str__(self):
        return self.text

