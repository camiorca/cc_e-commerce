import datetime
from django.contrib.auth.models import User
from .models import Product, CreditCard, Order, OrderItem, Payment, Shipment
from .validators import InfoValidations


class UtilityFunctions:

    def generate_order(self, user_id, total_value, address):
        order = Order.objects.create(
            user=User.objects.get(id=user_id),
            total_value=total_value,
            address=address,
            created_on=datetime.datetime.now()
        )

        return order

    def calculate_total_price(self, products):
        items = []
        try:
            total_cost = 0
            for item in products:
                total_cost += Product.objects.get(title=item['title']).price * item['quantity']
                order_item = {
                    'product_id': Product.objects.get(title=item['title']).id,
                    'quantity': item['quantity']
                }
                items.append(order_item)
            return {
                'items': items,
                'total_cost': total_cost
            }
        except:
            return []

    def apply_payment(self, payment_option, payment_methods, user_id):
        payments = []
        if payment_option:
            for item in payment_methods:
                if item['method'] == 'cc':
                    if InfoValidations.credit_card_user_validation(None, user_id) is True:
                        payment = {
                            'type': item['method'],
                            'amount': item['amount'],
                            'status': 'ordered'
                        }
                        payments.append(payment)
                    else:
                        return []
            return payments
        else:
            payment = {
                'type': payment_methods[0]['method'],
                'amount': payment_methods[0]['amount'],
                'status': 'ordered'
            }
            payments.append(payment)
            return payments
