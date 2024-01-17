from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import(
    Carousel, OfferText, Cards, TextOnHomepage)

# Create your views here.


def home(request):
    offertext = OfferText.objects.all()
    carousels = Carousel.objects.all()
    cards = Cards.objects.all()
    texts = TextOnHomepage.objects.all()
    
    context = {
        'offertext': offertext,
        'carousels': carousels,
        'cards': cards,
        'texts': texts,
    }
    
    return render(request, 'home/home.html', context)
