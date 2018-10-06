from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    sur_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Item(models.Model):
    name = models.CharField(max_length=500, blank=True, verbose_name='Товар')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Measure(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Единица')  # виды единиц могли бы быть сущностью
    rate = models.DecimalField(max_digits=9, decimal_places=3, verbose_name='Коэффициент')

    def __str__(self):
        return '{name}({rate})'.format(name=self.name, rate=self.rate)

    class Meta:
        verbose_name = 'Единица'
        verbose_name_plural = 'Единицы'


class Shop(models.Model):
    name = models.CharField(max_length=500, blank=True, verbose_name='Магазин')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class DocType(models.Model):
    name = models.CharField(max_length=500, blank=True, verbose_name='Тип документа')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'


class DocHeader(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE, verbose_name='Тип документа')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
    user_accepted = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Кто принял')


class DocTable(models.Model):
    doc_header = models.ForeignKey(DocHeader, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    amount = models.DecimalField(max_digits=15, decimal_places=3, verbose_name='Количество')
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE, verbose_name='Единица', default=None)


class Barcode(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    code128 = models.CharField(max_length=128, verbose_name='Code 128')

    class Meta:
        verbose_name = 'Штрихкод'
        verbose_name_plural = 'Штрихкоды'

