from django.db import models

class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    background_image = models.ImageField(upload_to='hero/')
    
    def __str__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')

class Client(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='clients/')

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=50)

class Newsletter(models.Model):
    email = models.EmailField()
