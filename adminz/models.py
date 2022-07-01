from django.db import models

# Create your models here.
class Banners(models.Model):

    carosel_hd1     = models.CharField(max_length=100,)
    carosel_hd2     = models.CharField(max_length=100,)
    carosel_hd3     = models.TextField(max_length=300,)
    ca_image1     = models.ImageField(upload_to = 'photos/banners')
    ca_image2     = models.ImageField(upload_to = 'photos/banners')

    banner_name1 = models.CharField(max_length=100,)
    banner_name2 = models.CharField(max_length=100,)
    banner_name3 = models.CharField(max_length=100,)
    bannerimg1 = models.ImageField(upload_to = 'photos/banners')
    bannerimg2 = models.ImageField(upload_to = 'photos/banners')
    bannerimg3 = models.ImageField(upload_to = 'photos/banners')

    fashiontrend_name1 = models.CharField(max_length=100,)
    fashiontrend_name2 = models.CharField(max_length=100,)
    fashiontrend_name3 = models.CharField(max_length=100,)
    insta_image1 = models.ImageField(upload_to = 'photos/banners') 
    insta_image2 = models.ImageField(upload_to = 'photos/banners') 
    insta_image3 = models.ImageField(upload_to = 'photos/banners') 

   

