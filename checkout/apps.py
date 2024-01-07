
from django.apps import AppConfig

class CheckoutConfig(AppConfig):
   
    name = 'checkout'

    def ready(self):
        import checkout.signals  # Importing signals to connect them