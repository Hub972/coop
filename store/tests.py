from django.contrib.auth import authenticate
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from mock import patch


from .models import InfoUser, Product, Bascket
from .utils import send_simple_message
from .views import book_product, change_book_status, index, display_my_product, detail, manage_book, book_detail, \
    change_info, modif_product_info, search_product
# Create your tests here.


class AppTestCase(TestCase):
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
        self.book.save()

    def test_index_page(self):
        """Test the main page"""
        factory = RequestFactory()
        req = factory.get(r'^$')
        req.user = self.clientUser
        response = index(req)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        """Test the register page """
        response = self.client.get(reverse('store:register'))
        self.assertEqual(response.status_code, 200)
        dataRegister = {
            'name': u'tester',
            'email': u'tester@email.com',
            'passwd': u'test',
            'confPasswd': u'test',
            'number': 3,
            'street': u'du test',
            'country': u'testland',
            'postalCode': 22345,
            'telephone': 339876545,
            'information': u'oui'
        }
        responsePost = self.client.post(reverse('store:register'), data=dataRegister)
        self.assertEqual(responsePost.status_code, 200)

    def test_connection_page(self):
        """Test page connect user"""
        response = self.client.get(reverse('store:conUser'))
        self.assertEqual(response.status_code, 200)
        dataConnection = {
            'name': u'tester',
            'passwd': u'test'
        }
        responsePost = self.client.post(reverse('store:conUser'), data=dataConnection)
        self.assertEqual(responsePost.status_code, 200)

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
        response = self.client.get(reverse('store:myPlace'))
        self.assertEqual(response.status_code, 302)

    def test_add_product_case(self):
        """test addProduct page"""
        response = self.client.get(reverse('store:addProduct'))
        self.assertEqual(response.status_code, 200)
        """test product exist"""
        self.assertIsNotNone(self.product)
        """Add a product"""
        dataProduct = {
            'name': u'cidre',
            'category': u'Boisson',
            'picture': u'other.png',
            'price': 0.50,
            'information': u'oui'
        }
        responsePost = self.client.post(reverse('store:addProduct'), data=dataProduct)
        self.assertEqual(responsePost.status_code, 200)

    def display_all_product(self):
        response = self.client.get(reverse('store:allProducts'))
        print(response.status_code)
        self.assertTemplateUsed(response, 'store/display_product_farmer.html')

    def test_display_prds_farmer(self):
        factory = RequestFactory()
        req = factory.get(r'diplay_product_farmer/$')
        req.user = self.farmer
        response = display_my_product(req)
        self.assertEqual(response.status_code, 200)

    def test_detail_product(self):
        factory = RequestFactory()
        req = factory.get('^(?P<product_id>[0-9]+)/$')
        req.user = self.clientUser
        response = detail(req, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_modif_product(self):
        responseGet = self.client.get(reverse('store:infoProduct', args=[self.product.id, ]))
        self.assertEqual(responseGet.status_code, 200)
        factory = RequestFactory()
        dataModifPrd = {
            'name': u'salade',
            'category': u'Fruit/Légume',
            'picture': u'salade.png',
            'price': 0.50,
            'information': u'oui'
        }
        req = factory.post(r'modif_product/(?P<prdId>[0-9]+)/$', data=dataModifPrd)
        req.user = self.farmer
        req.method = 'POST'
        response = modif_product_info(req, self.product.id)
        self.assertEqual(response.status_code, 302)

    def test_search_product(self):
        factory = RequestFactory()
        req = factory.post(r'^search_product/$', data={'query': u'salade'})
        req.user = self.clientUser
        req.method = 'POST'
        response = search_product(req)
        self.assertEqual(response.status_code, 200)

    def test_add_product_to_book(self):
        """book product"""
        factory = RequestFactory()
        quantity = {
            'quantity': 5
        }
        req = factory.post(r'^book/(?P<prd_id>[0-9]+)/', data=quantity)
        req.user = self.clientUser
        req.method = "POST"
        response = book_product(req, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_manage_book(self):
        factory = RequestFactory()
        req = factory.get(r'^my_book/$')
        req.user = self.farmer
        response = manage_book(req)
        self.assertEqual(response.status_code, 200)

    def test_book_detail(self):
        factory = RequestFactory()
        req = factory.get(r'^detail_book/(?P<idProduct>[0-9]+)/(?P<idBook>[0-9]+)$')
        req.user = self.farmer
        response = book_detail(req, self.product.id, self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_change_status_book(self):
        factory = RequestFactory()
        dataStatus = {
            'status': u'2'
        }
        req = factory.post(r'^change_status/(?P<bookId>[0-9]+)/', data=dataStatus)
        req.method = "POST"
        response = change_book_status(req, self.book.id)
        self.assertEqual(response.status_code, 302)

    def test_change_info_user(self):
        factory = RequestFactory()
        req = factory.get(r'^modif_info/$')
        req.user = self.clientUser
        response = change_info(req)
        self.assertEqual(response.status_code, 200)
        dataChangeInfo = {
            'name': u'le bon',
            'email': u'lebon@mail.com',
            'passwd': u'test',
            'confPasswd': u'test',
            'number': 3,
            'street': u'du test',
            'country': u'testland',
            'postalCode': 22345,
            'telephone': 339876545,
            'information': 'hello world'
        }
        reqPost = factory.post(r'^modif_info/$', data=dataChangeInfo)
        reqPost.user = self.clientUser
        responsePost = change_info(reqPost)
        self.assertEqual(responsePost.status_code, 302)

    def test_del_product(self):
        response = self.client.get(reverse('store:delPrd', args=[self.product.id, ]))
        self.assertEqual(response.status_code, 302)

    def test_if_user_logout(self):
        """Test disconnect user"""
        response = self.client.get(reverse('store:logOut'))
        self.assertEqual(response.status_code, 302)

    def test_display_terms(self):
        response = self.client.get(reverse('store:terms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/terms.html')


class MockCase(TestCase):
    RESPONSE = {
        'Response': {
            'request': {
                'status_code': 200,
                'url': 'https://api.mailgun.net/v3/sandbox6b9a603f2820431d882814909b076f40.mailgun.org/messages'
            }
        }
    }

    @patch('store.utils.send_simple_message', return_value=RESPONSE)
    def test_send_email(self, *args, **kwargs):
        msg = send_simple_message("ass.yon@laposte.net", "subject", "txt")
        self.assertIsNotNone(msg)
        self.assertEqual(msg.status_code, 200)
