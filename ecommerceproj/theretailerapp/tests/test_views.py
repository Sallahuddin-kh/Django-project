from django.test import TestCase
from django.urls import reverse
from theretailerapp.models import BasketItem , Product, Customer, Country

class TestViews(TestCase):
    def setUp(self):
        """
        Runs before all test to make the db in the state from
        where test cases can run. Makes the customer object and logs
        the customer In.
        """
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

    def test_item_added_from_basket(self):
        """
        Unit test to check if the quantity of product decreases when added to basket.
        """
        product = Product(product_name = 'test_product',
                         description = 'test description', 
                         price = 2000, 
                         available_quantity = 10,
                         is_active = True,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        
        product.save()   
        self.client.get(reverse('add_to_basket', kwargs={'product_id': str(product.id)}))
        product = Product.objects.get(id = product.id)
        if product.available_quantity == 9:
            assert True, "ITEM REDUCED WHEN ADDED TO BASKET"
        else:
            assert False, "ITEM NOT REDUCED WHEN ADDED TO BASKET"

    def test_item_removed_from_basket(self):
        """
        Unit test to check if the quantity of product increases when removed from basket.
        """
        product = Product(product_name = 'test_product6',
                         description = 'test description', 
                         price = 2000, 
                         available_quantity = 10,
                         is_active = True,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        product.save()   
        self.client.get(reverse('add_to_basket', kwargs={'product_id': str(product.id)}))
        basket_item = BasketItem.objects.filter(product = product).get()
        self.client.get(reverse('remove_from_basket', kwargs={'basketitem_id': str(basket_item.id)}))
        product = Product.objects.get(id = product.id)
        if product.available_quantity == 10:
            assert True, "ITEM ADDED BACK WHEN REMOVED FROM BASKET"
        else:
            assert False, "ITEM NOT ADDED BACK WHEN REMOVED FROM BASKET"

    def test_order_removed(self):
        """
        Unit test for the check if the quantity of products increase when order is cancelled.
        """
        product = Product(product_name = 'test_product_1',
                         description = 'test description_1', 
                         price = 2000, 
                         available_quantity = 20,
                         is_active = True,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        product.save()   
        self.client.get(reverse('add_to_basket', kwargs={'product_id': str(product.id)}))
        self.client.get(reverse('add_to_basket', kwargs={'product_id': str(product.id)}))
        self.client.post(reverse('place_order_form'), {'shipping_address': 'House Test'})
        product = Product.objects.get(id = product.id)
        self.client.get(reverse('cancel_order', kwargs={'order_id': 1}))
        product = Product.objects.get(id = product.id)
        if product.available_quantity == 20:
            assert True, "QUANTITY FOR ORDER ADDED ITEMS RESTORED"
        else:
            assert False, "QUANTITY FOR ORDER ADDED ITEMS NOT RESTORED"


    def test_non_active_listing(self):
        """
        Unit test to ensure if the product listing does not contain inactive products.
        """
        product1 = Product(product_name = 'test_product_3',
                         description = 'test description_3', 
                         price = 2000, 
                         available_quantity = 20,
                         is_active = False,
                         created_at = '2021-11-12',
                         updated_at = '2021-11-12')
        product1.save()
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
                assert False,"INACTIVE PRODUCTS STILL BEING SHOWN IN THE LISTING"
        if flag:
            assert True , "INACTIVE PRODUCTS NOT SHOWN IN THE LISTING"
