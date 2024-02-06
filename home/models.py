from django.db import models
from django.utils import timezone

# Create your models here.

class OfferText(models.Model):
    
    class Meta:
        """
        adjust the name.
        override django from adding s to the end of the classname
        this will be shown on django admin.
        """
        verbose_name_plural = 'Offer Text'
        
    offer_title1 = models.TextField(max_length=200, null=True, blank=True)
    offer_title2 = models.TextField(max_length=200, null=True, blank=True)
    offer_title3 = models.TextField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return  self.offer_title1
    
# Carousel
class Carousel(models.Model):
    
    class Meta:
        """
        adjust the name.
        this will be shown on django admin.
        """
        verbose_name_plural = 'Carousel'
        
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(upload_to='carousel_videos/', null=True, blank=True)
    carousel_number = models.IntegerField(null=False, blank=False, default='0')
    image_class = models.TextField(max_length=180, default='If carousel number = 1 then image class = image_first and css_class = first')
    title = models.TextField(max_length=500, null=True, blank=True,)
    description = models.TextField(null=True, blank=True, max_length=10000)
    extra_info = models.TextField(null=True, blank=True, max_length=1000)
    btn_main_first = models.TextField(max_length=200, null=True, blank=True, default='Important : use this button for 1st carousel image only')
    btn_sub_first = models.TextField(max_length=200, null=True, blank=True, default='Important : use this button for 1st carousel image only')
    btn_main_second = models.TextField(max_length=200, null=True, blank=True, default='Important : use this button for 2nd carousel image only')
    btn_sub_second = models.TextField(max_length=200, null=True, blank=True, default='Important : use this button for 2nd carousel image only')
    btn_main_third = models.TextField(max_length=200, null=True, blank=True, default='Important : use this button for 3th carousel image only')
    btn_sub_third = models.TextField(max_length=200, null=True, blank=True, default='Important : use this button for 3th carousel image only')
    css_class = models.TextField(max_length=50)
    
    def has_image_or_video(self):
        return self.image or self.video

    class Meta:
        ordering = ['carousel_number']
    
    def __str__(self):
        return  self.title
    

class TextOnHomepage(models.Model):
    class Meta:
        
        """
        adjust the name.
        override django from adding s to the end of the classname
        this will be shown on django admin.
        """
        verbose_name_plural = 'Text below Carousel'
    
    title = models.TextField(max_length=500, null=True, blank=True)
    heading = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    btn_text = models.TextField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return  self.title
    
  
class Cards(models.Model):
    
    class Meta:
        """
        adjust the name.
        override django from adding s to the end of the classname
        this will be shown on django admin.
        """
        verbose_name_plural = 'Card'
    
    id = models.AutoField(primary_key=True)
    image = models.ImageField(null=True, blank=True)
    title = models.TextField(max_length=500, null=True, blank=True)
    heading = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    btn_card = models.TextField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.title
    