from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from checkout.webhook_handler import StripeWebhookHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listen to Stripe webhooks"""
    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # get the webhook data and verify signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
            )

    except ValueError as e:
        # invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        return HttpResponse(status=400)

    except Exception as e:
        return HttpResponse(content=e, status=400)
        
    # set up a webhook handler
    handler = StripeWebhookHandler(request)

    # map webhook events to relevant functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_failed,
    }

    # get the webhook type from Stripe
    event_type = event['type']

    # use the generic one by default and
    # if specific handler, get it from the event map
    event_handler = event_map.get(event_type, handler.handle_event)

    # call event handler with the event
    response = event_handler(event)
    return response