from django.test import TestCase
from django.urls import reverse
from theretailerapp.models import BasketItem , Product, Customer, Country, ApprovalStatus

class TestViews(TestCase):
    basket_instance = []
    def setUp(self):
        country = Country(country_name = 'Pakistan')
        country.save()
        customer = Customer(first_name = 'firstname',
                            last_name = 'lastname',
                            shipping_address = "Ship",
                            billing_address = 'bill',
                            password = '12345678',
                            ph_number = '+92345654345',
                            email = 'test@gmail.com',
                            counrty = country,
                            created_at =  '2021-11-12',
                            updated_at =  '2021-11-12')
        self.cus = customer
        customer.save()
        s = self.client.session
        s.update({
            "email": customer.email,
            "first_name": customer.first_name,
        })
        s.save()
        approval = ApprovalStatus(approval_status = 'pending')
        approval.save()
        approval = ApprovalStatus(approval_status = 'cancelled')
        approval.save()

    def test_item_added_and_removed_to_basket(self):
        product = Product(product_name = 'test_product',
                         description = 'test description', 
                         price = 2000, 
                         available_quantity = 10,
                         is_active = True,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        
        product.save()   
        self.client.get(reverse('add_to_basket', kwargs={'id': str(product.id)}))
        product = Product.objects.get(id = product.id)
        assert product.available_quantity == 9
        basket_item = BasketItem.objects.filter(product = product).get()
        self.client.get(reverse('remove_from_basket', kwargs={'id': str(basket_item.id)}))
        product = Product.objects.get(id = product.id)
        assert product.available_quantity == 10

    def test_order_removed_from_basket(self):
        
        product = Product(product_name = 'test_product_1',
                         description = 'test description_1', 
                         price = 2000, 
                         available_quantity = 20,
                         is_active = True,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        product.save()   
        self.client.get(reverse('add_to_basket', kwargs={'id': str(product.id)}))
        self.client.get(reverse('add_to_basket', kwargs={'id': str(product.id)}))
        self.client.post(reverse('place_order_form'), {'shipping_address': 'House Test'})
        product = Product.objects.get(id = product.id)
        self.client.get(reverse('cancel_order', kwargs={'id': 1}))
        product = Product.objects.get(id = product.id)
        assert product.available_quantity == 20

    def test_non_active_listing(self):
        product1 = Product(product_name = 'test_product_3',
                         description = 'test description_3', 
                         price = 2000, 
                         available_quantity = 20,
                         is_active = False,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        product1.save()
        product1_id = product1.id
        product2 = Product(product_name = 'test_product_4',
                         description = 'test description_4', 
                         price = 2000, 
                         available_quantity = 20,
                         is_active = True,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        product2.save()
        product3 = Product(product_name = 'test_product_5',
                         description = 'test description_5', 
                         price = 2000, 
                         available_quantity = 20,
                         is_active = True,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        product3.save()
        response_data = self.client.get(reverse('product'))
        product_list = response_data.context['product_list']
        flag = True
        for product_item in product_list:
            if product_item.is_active == False:
                flag = False
                assert False
        if flag:
            assert True
