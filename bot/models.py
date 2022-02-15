from tabnanny import verbose
from django.db import models
from ckeditor.fields import RichTextField 

# Create your models here.
class Application(models.Model):
    fullname = models.CharField(max_length=40, null = True)
    fakultet = models.CharField(max_length=100, null = True)
    phone_number = models.CharField(max_length = 20, null = True)

    def __str__(self):
        return self.fullname
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
    

class Facultet(models.Model):
    name = models.CharField(max_length=50)
    about = RichTextField()

    def __str__(self):
        template = '{0.name} {0.about}'
        return template.format(self)
    
    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'


class Super(models.Model):
    price = models.CharField(max_length=40)

    def __str__(self):
        return self.price
    class Meta:
        verbose_name='Super'
    

class About(models.Model):
    about = RichTextField()

    def __str__(self):
        return self.about
    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'Abouts'