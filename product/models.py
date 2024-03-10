from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=170, blank=False, null=False, default=None)
    slug = models.SlugField(unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=170, null=True, blank=True)
    category_image = models.ImageField(upload_to='categories', default='default_image.jpg')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name

    def get_display_name(self):
        return self.display_name


class Product(models.Model):
    
    PRODUCT_FOR_CHOICES = (
        ('Men', 'Men'),
        ('Woman', 'Woman'),
        ('unisex', 'unisex'),
        ('Animals', 'Animals'),
        ('Accessories', 'Accessories'),
        ('Others', 'Others'),
    )
    
    product_name = models.CharField(max_length=200, unique=True)
    product_for = models.CharField(
        choices= PRODUCT_FOR_CHOICES, default='', max_length=50,  null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=800, blank=True)
    selling_price = models.IntegerField()
    old_price = models.IntegerField(default='0')
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.product_name} - {self.product_for}"
    

class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(is_active=True).values_list('size', flat=True).distinct()

    def colors(self):
        return super(VariationManager, self).filter(is_active=True).values_list('color', flat=True).distinct()


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()
    
    def __str__(self):
        return f"{self.product.product_name} - {self.product.product_for} - {self.size} - {self.color}"

    def get_stock(self):
        return self.stock_quantity
    
    def increase_stock(self, quantity):
        """
        Increase the stock quantity by the given amount.
        """
        self.stock_quantity += quantity
        self.save()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to='products/images/')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    
         
    def __str__(self):
        if self.variation:
            return f"{self.product.product_name} - {self.product.product_for} - {self.variation.color} - ProductImage {self.pk}"
        else:
            return f"{self.product.product_name} - {self.product.product_for} - Forgot to choose Variation ? - ProductImage {self.pk}"

class WomanProduct(Product):
   pass
    
class ManProduct(Product):
  pass
    
class UnisexProduct(Product):
   pass
    