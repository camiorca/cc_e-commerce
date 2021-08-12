from .models import Product, Order, Payment, OrderItem, Shipment, CreditCard


class InfoValidations():
    def credit_card_user_validation(self, user_id):
        try:
            if CreditCard.objects.filter(user=user_id) is not None:
                return True
        except:
            return False