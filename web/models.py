from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    sur_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)


class Item(models.Model):
    name = models.CharField(max_length=500, blank=True, verbose_name='Товар')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)


class Shop(models.Model):
    name = models.CharField(max_length=500, blank=True, verbose_name='Магазин')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)


class DocType(models.Model):
    name = models.CharField(max_length=500, blank=True, verbose_name='Тип документа')


class DocHeader(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE, verbose_name='Тип документа')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
    user_accepted = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Кто принял')


class DocTable(models.Model):
    doc_header = models.ForeignKey(DocHeader, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    amount = models.DecimalField(max_digits=15, decimal_places=3)
