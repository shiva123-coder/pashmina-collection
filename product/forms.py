from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        display_names = [(c.id, c.get_display_name()) for c in categories]

        self.fields['category'].choices = display_names
        
        
## Explanation for above code:

## The __init__ method in Python is a special method (also known as a "dunder" method, short for "double underscore") that is automatically called when an object of a class is created.
# It stands for "initialize" and is commonly used to perform setup or initialization tasks for the object.


## super().__init__(*args, **kwargs): Calls the __init__ method of the parent class (presumably a form or a class from which this form is derived).
# This is important to ensure that the initialization of the base class is completed before proceeding with any additional setup.

## categories = Category.objects.all(): Retrieves all objects from the Category model (assuming it's a Django model).

## display_names = [(c.id, c.get_display_name()) for c in categories]: Creates a list of tuples containing category IDs and their display names. It seems like get_display_name() is a method of the Category model,
# which is used to obtain a display name for each category.

## self.fields['category'].choices = display_names: Sets the choices for the 'category' field of the form to the list of display names obtained earlier. This is common in Django forms,
# where you populate choices dynamically, for example, from the database.