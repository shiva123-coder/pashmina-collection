from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import stripe

from .models import Order, OrderLineItem
from product.models import Product
from profiles.models import UserProfile

import json
import time


class StripeWebhookHandler:
    """stripe webhook handler"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        customer_email = order.email
        subject = render_to_string(
            'checkout/email_confirmation/email_confirmation_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/email_confirmation/email_confirmation_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """handle unknown webhook event"""
        return HttpResponse(
            content=f"Unhandled webhook recieved : {event['type']}",
            status=200
            )

    def handle_payment_intent_succeeded(self, event):
        """handle succedeed payment intent webhook from stripe"""
        intent = event.data.object
        payment_intent_id = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        
        billing_details = stripe_charge.billing_details
        delivery_details = intent.shipping
        sum_total = round(stripe_charge.amount / 100, 2)

        for field, value in delivery_details.address.items():
            if value == "":
                delivery_details.address[field] = None

        """
        profile information update once user
        choose the option to save their
        information by checking save_info box
        on the checkout form
        """
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.user_full_name = delivery_details.name
                profile.user_contact_number = delivery_details.phone
                profile.user_address = delivery_details.address.line1
                profile.user_postal_code = delivery_details.address.postal_code
                profile.save()

        order_exists = False
        attempt = 1

        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=delivery_details.name,
                    email__iexact=billing_details.email,
                    contact_number__iexact=delivery_details.phone,
                    street_address__iexact=delivery_details.address.line1,
                    postal_code__iexact=delivery_details.address.postal_code,
                    sum_total=sum_total,
                    original_basket=basket,
                    stripe_payment_intent_id=payment_intent_id,
                )

                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: \
                    Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                        full_name=delivery_details.name,
                        user_profile=profile,
                        contact_number=delivery_details.phone,
                        email=billing_details.email,
                        street_address=delivery_details.address.line1,
                        postal_code=delivery_details.address.postal_code,
                        original_basket=basket,
                        stripe_payment_intent_id=payment_intent_id,
                    )

                for product_id, quantity in json.loads(basket).items():

                    product = Product.objects.get(id=product_id)

                    order_line_item = OrderLineItem(
                        order=order, product=product,
                        quantity=quantity,
                        )

                    order_line_item.save()

            except Exception as e:

                if order:
                    order.delete()
                return HttpResponse(content="Webhook recieved \
                    : {event['type']} | ERROR : {e}", status=500)

        self._send_confirmation_email(order)

        return HttpResponse(
            content=f"Webhook recieved : {event['type']} | \
                SUCCESS: Created order in webhook", status=200)

    def handle_payment_intent_failed(self, event):
        """handle failed payment intent webhook from stripe"""
        return HttpResponse(
            content=f"Webhook recieved : {event['type']}", status=200)
        
