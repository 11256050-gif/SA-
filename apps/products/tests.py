from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Order, Product


class CreateOrderSpecificationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.seller = user_model.objects.create_user(username='seller', password='pass')
        self.buyer = user_model.objects.create_user(username='buyer', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(self.buyer)

    def create_product(self, specifications):
        return Product.objects.create(
            seller=self.seller,
            name='Test product',
            price='100.00',
            stock=5,
            status='onsale',
            specifications=specifications,
        )

    def post_order(self, product, selected_specification):
        return self.client.post(
            '/api/products/orders/create_order/',
            {
                'product_id': product.id,
                'quantity': 1,
                'selected_specification': selected_specification,
                'recipient_name': 'Buyer',
                'recipient_phone': '0912345678',
                'recipient_address': 'Taipei',
                'payment_method': 'cod',
            },
            format='json',
        )

    def test_accepts_normalized_specification_with_chinese_separators(self):
        product = self.create_product('01 紅棕，02 奶茶、03 玫瑰')

        response = self.post_order(product, '  02   奶茶  ')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.get().selected_specification, '02 奶茶')

    def test_auto_selects_single_specification_when_frontend_sends_blank(self):
        product = self.create_product('阿災')

        response = self.post_order(product, '')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.get().selected_specification, '阿災')

    def test_public_product_list_excludes_out_of_stock_products(self):
        available = self.create_product('')
        Product.objects.create(
            seller=self.seller,
            name='Sold out product',
            price='100.00',
            stock=0,
            status='onsale',
            specifications='',
        )

        response = self.client.get('/api/products/products/')

        self.assertEqual(response.status_code, 200)
        product_ids = [item['id'] for item in response.json()['results']]
        self.assertEqual(product_ids, [available.id])
