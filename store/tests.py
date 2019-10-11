import requests
from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from mock import patch


from .models import InfoUser, Product, Bascket
from .utils import send_simple_message
# Create your tests here.


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        """Test the main page """
        response = self.client.get(reverse('store:index'))
        self.assertEqual(response.status_code, 200)


class RegisterConnectionPageTestCase(TestCase):
    def setUp(self):
        self.clientUser = User()
        self.clientUser.username = 'Nath'
        self.clientUser.email = 'nath@mail.com'
        self.clientUser.password = 'passwd'
        self.clientUser.save()
        self.infoUser = InfoUser()
        self.infoUser.number = 3
        self.infoUser.street = "la campagne"
        self.infoUser.country = "Lamballe"
        self.infoUser.postalCode = "22400"
        self.infoUser.telephone = 43344543
        self.infoUser.information = "belle femme"
        self.infoUser.idUser = self.clientUser
        self.infoUser.save()
        self.farmer = User.objects.create_user(username='farmer', email='farmer@mail.com', password='passwd', is_staff=True)
        self.infoFarmer = InfoUser()
        self.infoFarmer.number = 1
        self.infoFarmer.street = "de la campagne"
        self.infoFarmer.country = "Lamballe"
        self.infoFarmer.postalCode = 22400
        self.infoFarmer.telephone = 675454323
        self.infoFarmer.information = "Mieux que seguin"
        self.infoFarmer.idUser = self.farmer
        self.infoFarmer.save()
        self.product = Product()
        self.product.name = "cidre de bretagne"
        self.product.category = "Boisson"
        self.product.price = 1.00
        self.product.picture = 'media/pic/cidre.jpeg'
        self.product.information = "Bon produit"
        self.product.idSeller = self.farmer
        self.product.save()
        self.book = Bascket()
        self.book.cmdNumber = 6
        self.book.quantity = 3
        self.book.idClient = self.infoUser
        self.book.idSeller = self.farmer
        self.book.idProduct = self.product

    def test_register_page(self):
        """Test the register page """
        response = self.client.get(reverse('store:register'))
        self.assertEqual(response.status_code, 200)

    def test_connection_page(self):
        """Test page connect user"""
        response = self.client.get(reverse('store:conUser'))
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        """Test put user in database"""
        bot = User.objects.get_by_natural_key(username='Nath')
        self.assertIsNotNone(bot)
        self.assertEqual(bot.id, self.infoUser.idUser.id)
        self.assertEqual(bot.is_staff, False)
        """test my place page"""
        response = self.client.get(reverse('store:myPlace'))
        self.assertEqual(response.status_code, 302)

    def test_register_farmer(self):
        """test farmer object"""
        self.assertIsNotNone(self.farmer)
        self.assertEqual(self.farmer.is_staff, True)
        self.assertEqual(self.infoFarmer.postalCode, 22400)
        self.assertEqual(self.infoFarmer.idUser.id, self.farmer.id)
        userauth = authenticate(username='farmer', password='passwd')
        self.assertIsNotNone(userauth)

    def test_my_place_farmer(self):
        """test my place page"""
        response = self.client.get(reverse('store:myPlace'))
        self.assertEqual(response.status_code, 302)

    def test_product_case(self):
        """test addProduct page"""
        response = self.client.get(reverse('store:addProduct'))
        self.assertEqual(response.status_code, 200)
        """test product exist"""
        self.assertIsNotNone(self.product)

    def test_add_product_to_book(self):
        """book product"""
        self.assertEqual(self.book.idProduct.id, self.product.id)

    def change_status_book(self):
        book = Bascket.objects.get(idSeller=self.farmer)
        status = book.status
        book.status = 3
        book.save()
        self.assertNotEqual(status, book.status)

    def test_if_user_logout(self):
        """Test disconnect user"""
        response = self.client.get(reverse('store:logOut'))
        self.assertEqual(response.status_code, 302)


class MockCase(TestCase):
    RESPONSE = requests.post(
        "https://api.mailgun.net/v3/sandbox6b9a603f2820431d882814909b076f40.mailgun.org/messages",
        auth=("api", "API_KEY"),
        data={"from": "Mailgun Sandbox <noreply@sandbox6b9a603f2820431d882814909b076f40.mailgun.org>",
              "to": "dst",
              "subject": "subject",
              "text": "txt"})

    @patch('store.utils.send_simple_message', return_value=RESPONSE)
    def test_send_email(self, *args, **kwargs):
        msg = send_simple_message("dst", "subject", "txt")
        self.assertIsNotNone(msg)






