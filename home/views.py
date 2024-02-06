from django.conf import settings
from django.contrib import messages
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.core.mail import send_mail, BadHeaderError
from .models import OfferText, Carousel, Cards, TextOnHomepage
from .forms import ContactForm

def home(request):
    offertext = OfferText.objects.all()
    carousels = Carousel.objects.all()
    cards = Cards.objects.all()
    texts = TextOnHomepage.objects.all()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            subject = 'Enquiry'
            body = {
                'full_name': form.cleaned_data['full_name'],
                'message': form.cleaned_data['message'],
                }
            sender_email = form.cleaned_data['email']
            message = '\n'.join(body.values())         
            
        try:
            send_mail(
                subject, message, sender_email,  ['sb4_cbu@yahoo.com', 'cia.ribka@gmail.com'])
            return render(request, 'home/success.html')
        except BadHeaderError:         
            return HttpResponse('Invalid header found.')
    else:
        form = ContactForm()
    
    context = {
        'offertext': offertext,
        'carousels': carousels,
        'cards': cards,
        'texts': texts,
        'form': form,
    }
    
    return render(request, 'home/home.html', context)