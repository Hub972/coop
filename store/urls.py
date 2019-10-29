from django.conf.urls import url

from . import views
app_name = 'store'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^connection/$', views.connect_user, name='conUser'),
    url(r'^my_place/$', views.my_place, name='myPlace'),
    url(r'^add_product/$', views.add_product_to_db, name='addProduct'),
    url(r'diplay_product_farmer/$', views.display_my_product, name='displayProductFarmer'),
    url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^book/(?P<prd_id>[0-9]+)/$', views.book_product, name='book'),
    url(r'^display_all_products', views.display_all_products, name='allProducts'),
    url(r'^my_book/$', views.manage_book, name='manageBook'),
    url(r'^detail_book/(?P<idProduct>[0-9]+)/(?P<idBook>[0-9]+)$', views.book_detail, name='detailBook'),
    url(r'^change_status/(?P<bookId>[0-9]+)/$', views.change_book_status, name='changeStatus'),
    url(r'^modif_info/$', views.change_info, name='modifInfo'),
    url(r'modif_product/(?P<prdId>[0-9]+)/$', views.modif_product_info, name='infoProduct'),
    url(r'del_product/(?P<prdId>[0-9]+)/$', views.del_product, name='delPrd'),
    url(r'^logout_user/$', views.logout_user, name='logOut'),
    url(r'^search_product/$', views.search_product, name='search'),
    url(r'^$', views.index, name='index'),
    url(r'^terms/$', views.display_terms, name='terms')
]
