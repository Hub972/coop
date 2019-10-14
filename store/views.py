from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.models import User
from django.db import transaction
import random

from .models import InfoUser, Product, Bascket
from .forms import RegisterForm, ParagraphErrorList, ProfileForm, ProductForm, BascketForm, StatusForm, \
    RegisterModifForm, ProductModifForm, SearchForm
from .utils import send_simple_message
# Create your views here.


def index(request):
    form = SearchForm()
    return render(request, 'store/index.html', context={'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['passwd']
            confPasswd = form.cleaned_data['confPasswd']
            num = form.cleaned_data['numero']
            street = form.cleaned_data['rue']
            country = form.cleaned_data['ville']
            postalCode = form.cleaned_data['codePostal']
            tel = form.cleaned_data['telephone']
            information = form.cleaned_data['information']
            if passwd == confPasswd:
                with transaction.atomic():
                    u = User.objects.create_user(username=name, email=email, password=passwd)
                    u.save()
                    infUser = InfoUser()
                    infUser.number = num
                    infUser.street = street
                    infUser.country = country
                    infUser.postalCode = postalCode
                    infUser.telephone = tel
                    infUser.information = information
                    infUser.idUser = u
                    infUser.save()
                    return render(request, 'store/index.html', context={'thanks': True, 'name': name})
            else:
                form = RegisterForm()
                context = {
                    'form': form,
                    'badInf': True
                }
                return render(request, 'store/register.html', context)

    form = RegisterForm(auto_id=False)
    return render(request, 'store/register.html', context={'form': form})


def connect_user(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form.cleaned_data['name']
            passwd = form.cleaned_data['passwd']
            user = authenticate(username=name, password=passwd)
            if user is None:
                form = ProfileForm
                context = {
                    'form': form
                }
                return render(request, 'store/connection.html', context)
            else:
                login(request, user)
                form = SearchForm()
                context = {'form': form}
                if user.is_staff:
                    context = {'isStaff': True,
                               "form": form
                               }
                return render(request, 'store/index.html', context)
    form = ProfileForm()
    return render(request, 'store/connection.html', context={'form': form})


@login_required(login_url='store:conUser')
def my_place(request):
    user = request.user.id
    infUser = get_object_or_404(User, pk=user)
    name = infUser.username
    email = infUser.email
    infUser2 = InfoUser.objects.get(idUser=user)
    number = infUser2.number
    street = infUser2.street
    country = infUser2.country
    postalCode = infUser2.postalCode
    information = infUser2.information
    tel = infUser2.telephone
    isStaff = False
    if infUser.is_staff:
        isStaff = True
    context = {
        'name': name,
        'email': email,
        'number': number,
        'street': street,
        'country': country,
        'postalCode': postalCode,
        'information': information,
        'tel': tel,
        'isStaff': isStaff
    }
    return render(request, 'store/my_place.html', context)


def add_product_to_db(request):
    form = ProductForm()
    context = {'form': form}
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, error_class=ParagraphErrorList)
        if form.is_valid():
            name = form.cleaned_data['name']
            cat = form.cleaned_data['category']
            dispo = form.cleaned_data['disponibility']
            pic = form.cleaned_data['picture']
            price = form.cleaned_data['price']
            inf = form.cleaned_data['information']
            userId = request.user.id
            user = get_object_or_404(User, pk=userId)
            with transaction.atomic():
                prd = Product.objects.create(
                    name=name,
                    category=cat,
                    disponibility=dispo,
                    picture=pic,
                    information=inf,
                    price=price,
                    idSeller=user
                )
                prd.save
                if user.is_staff:
                    context = {'isStaff': True, 'prdAdd': True}
                return render(request, 'store/index.html', context)
    return render(request, 'store/farmer_count.html', context)


def display_my_product(request):
    user = request.user.id
    product = get_list_or_404(Product, idSeller=user)
    seller = get_object_or_404(User, pk=user)
    infoSeller = get_object_or_404(InfoUser, idUser=user)
    context = {
        'product': product,
        'seller': seller,
        'infoSeller': infoSeller
    }
    return render(request, 'store/display_product_farmer.html', context)


def detail(request, product_id):
    userId = request.user.id
    product = get_object_or_404(Product, pk=product_id)
    staff = False
    if userId:
        user = get_object_or_404(User, pk=userId)
        if user.is_staff:
            staff = True
    infoSeller = get_object_or_404(InfoUser, idUser=product.idSeller)
    form = BascketForm()
    context = {
        'prd': product,
        'info': infoSeller,
        'form': form,
        'staff': staff,
        'userId': userId
    }
    return render(request, 'store/detail.html', context)


@login_required(login_url='store:conUser')
def book_product(request, prd_id):
    if request.method == "POST":
        form = BascketForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            qunty = form.cleaned_data['quantity']
            userId = request.user.id
            user = get_object_or_404(InfoUser, idUser=userId)
            prd = get_object_or_404(Product, pk=prd_id)
            check = False
            while not check:
                cmd = random.randint(0000000, 9999999)
                bookList = Bascket.objects.all()

                checkList = []
                for book in bookList:
                    checkList.append(book.cmdNumber)
                if cmd in checkList:
                    pass
                else:
                    check = True

            with transaction.atomic():
                sellerId = prd.idSeller
                prd = Bascket.objects.create(
                    cmdNumber=cmd,
                    quantity=qunty,
                    idProduct=prd,
                    idClient=user,
                    idSeller=sellerId
                )
                prd.save()

            product = get_object_or_404(Product, pk=prd_id)
            seller = User.objects.filter(username=product.idSeller)
            #dst = seller.email
            dst = "ass.yon@laposte.net"
            subject = "Nouvelle commande de la coop"
            txt = f"Une commande a été éffectuée sont numéro est le {cmd}.\n" \
                  f"Je vous remercie d'avance pour votre réactivitée." \
                  f"Cordialement la coop de Lamballe.  "
            send_simple_message(dst, subject, txt)
            context = {
                'info': seller
            }
            return render(request, 'store/confirmation.html', context)


def display_all_products(request):
    products = get_list_or_404(Product)
    return render(request, 'store/display_product_farmer.html', context={'product': products})


def change_book_status(request, bookId):
    if request.method == 'POST':
        form = StatusForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            with transaction.atomic():
                status = form.cleaned_data['status']
                book = get_object_or_404(Bascket, pk=bookId)
                book.status = status
                book.save()
                if status == '3':
                    dst = "ass.yon@laposte.net"
                    subject = "Suivi de votre commande lacoop"
                    txt = f"Votre commande {book.cmdNumber} est prête vous pouvez allez sur votre profile pour toutes " \
                          f"les informations.\n Merci de votre confiance. "
                    send_simple_message(dst, subject, txt)
                return redirect('../my_book/')


def manage_book(request):
    userId = request.user.id
    user = get_object_or_404(User, pk=userId)
    infUser = get_object_or_404(InfoUser, idUser=userId)
    staff = False

    if user.is_staff:
        staff = True
        book = get_list_or_404(Bascket, idSeller=userId)
    else:
        book = get_list_or_404(Bascket, idClient=infUser)
    context = {
        'book': book,
        'staff': staff

    }
    return render(request, 'store/my_book.html', context)


def book_detail(request, idProduct, idBook):
    userId = request.user.id
    user = get_object_or_404(User, pk=userId)
    staff = False
    if user.is_staff:
        staff = True
    product = get_object_or_404(Product, pk=idProduct)
    seller = User.objects.filter(pk=product.idSeller.id)
    book = get_object_or_404(Bascket, pk=idBook)
    client = book.idClient
    infoClient = get_object_or_404(InfoUser, pk=client.id)
    dst = get_object_or_404(User, pk=infoClient.idUser.id)
    infoSeller = InfoUser.objects.filter(idUser=product.idSeller.id)
    form = StatusForm()
    for p in infoSeller:
        number = p.number
        street = p.street
        country = p.country
        postalCode = p.postalCode
        tel = p.telephone
    for p in seller:
        email = p.email
        name = p
    ttc = product.price * book.quantity
    context = {
        'prd': product,
        'infoc': infoClient,
        'info': infoSeller,
        'name': name,
        'email': email,
        'number': number,
        'street': street,
        'country': country,
        'postalCode': postalCode,
        'tel': tel,
        'form': form,
        'staff': staff,
        'user': dst,
        'idBook': idBook,
        'status': book.status,
        'quant': book.quantity,
        'ttc': ttc
    }
    return render(request, 'store/detail_book.html', context)


@login_required(login_url='store:conUser')
def change_info(request):
    """The user can modify the own information"""
    user = request.user.id
    infUser = get_object_or_404(User, pk=user)
    infUser2 = InfoUser.objects.get(idUser=user)
    if request.method == 'POST':
        form = RegisterModifForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            with transaction.atomic():
                if form.cleaned_data['nom']:
                    infUser.username = form.cleaned_data['nom']
                if form.cleaned_data['email']:
                    infUser.email = form.cleaned_data['email']
                if form.cleaned_data['passwd']:
                    if form.cleaned_data['passwd'] == form.cleaned_data['confPasswd']:
                        infUser.password = form.cleaned_data['passwd']
                infUser.save()
                if form.cleaned_data['numero']:
                    infUser2.number = form.cleaned_data['numero']
                    infUser2.save()
                if form.cleaned_data['rue']:
                    infUser2.street = form.cleaned_data['rue']
                    infUser2.save()
                if form.cleaned_data['ville']:
                    infUser2.country = form.cleaned_data['ville']
                    infUser2.save()
                if form.cleaned_data['codePostal']:
                    infUser2.postalCode = form.cleaned_data['codePostal']
                    infUser2.save()
                if form.cleaned_data['telephone']:
                    infUser2.telephone = form.cleaned_data['telephone']
                    infUser2.save()
                if form.cleaned_data['information']:
                    infUser2.information = form.cleaned_data['information']
                    infUser2.save()
                return redirect('../my_place/')
    else:
        #user info
        name = infUser.username
        email = infUser.email

        number = infUser2.number
        street = infUser2.street
        country = infUser2.country
        postalCode = infUser2.postalCode
        information = infUser2.information
        tel = infUser2.telephone
        isStaff = False
        if infUser.is_staff:
            isStaff = True
        # form for change info
        form = RegisterModifForm()
        context = {
            'name': name,
            'email': email,
            'number': number,
            'street': street,
            'country': country,
            'postalCode': postalCode,
            'information': information,
            'tel': tel,
            'isStaff': isStaff,
            'form': form
        }
        return render(request, 'store/modif_info.html', context)


def modif_product_info(request, prdId):
    userId = request.user.id
    product = get_object_or_404(Product, pk=prdId)
    infoSeller = get_object_or_404(InfoUser, idUser=product.idSeller)
    if request.method == 'POST':
        form = ProductModifForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            with transaction.atomic():
                if form.cleaned_data['name']:
                    product.name = form.cleaned_data['name']
                    product.save()
                if form.cleaned_data['category']:
                    product.category = form.cleaned_data['category']
                    product.save()
                if form.cleaned_data['disponibility']:
                    product.disponibility = form.cleaned_data['disponibility']
                    product.save()
                if form.cleaned_data['picture']:
                    product.picture = form.cleaned_data['picture']
                    product.save()
                if form.cleaned_data['price']:
                    product.price = form.cleaned_data['price']
                    product.save()
                if form.cleaned_data['information']:
                    product.information = form.cleaned_data['information']
                    product.save()
                return redirect(f'/store/{prdId}/')
    else:
        form = ProductModifForm()
        context = {
            'prd': product,
            'info': infoSeller,
            'form': form

        }
        return render(request, 'store/modif_product.html', context)


def del_product(request, prdId):
    """Farmer can del product here"""
    prd = get_object_or_404(Product, pk=prdId)
    prd.delete()
    return redirect('/store/diplay_product_farmer/')


def logout_user(request):
    logout(request)
    return redirect('/')


def search_product(request):
    if request.method == 'POST':
        form = SearchForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            query = form.cleaned_data['query']
            if not query:
                prds = Product.objects.all()
            else:
                prds = Product.objects.filter(name__icontains=query)
                if not prds.exists():
                    prds = None
                context = {
                    'prds': prds
                }
                return render(request, 'store/display_search.html', context)







