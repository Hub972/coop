from django.contrib import admin

from .models import InfoUser, Product, Bascket, Delivery

# Register your models here.
@admin.register(InfoUser)
class InfoUserRegister(admin.ModelAdmin):
    pass


@admin.register(Bascket)
class BookRegister(admin.ModelAdmin):
    pass
