from django.core.management.base import BaseCommand
from django.utils import timezone
from theretailerapp.models import Order, Customer
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, help='Define a username prefix', )
        parser.add_argument('-i', '--id', type=str, help='Define a username prefix', )
    def handle(self, *args, **kwargs):
        email = kwargs['email']
        id = kwargs['id']
        if id:
            try:
                orders = Order.objects.filter(customer = id)
                for order in orders:
                    self.stdout.write("Order id: %s " %order.id)
                    self.stdout.write("Order date: %s " %order.placed_at)
                    self.stdout.write("-------------------")
            except Exception as e:
                self.stdout.write("No id orders found")
        elif email :
            try:
                customer = Customer.objects.get(email = email)
                orders = Order.objects.filter(customer = customer.id)
                for order in orders:
                        self.stdout.write("Order id: %s " %order.id)
                        self.stdout.write("Order date: %s " %order.placed_at)
                        self.stdout.write("-------------------")
            except Exception as e:
                self.stdout.write("No email orders found")