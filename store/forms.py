from django import forms
from django.forms.utils import ErrorList


class RegisterForm(forms.Form):
    nom = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Nom'}),
        required=True,

    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-group', 'placeholder': 'Email'}),
        required=True,

    )
    passwd = forms.CharField(
        label='',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'}),
        required=True
    )
    confPasswd = forms.CharField(
        label='',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe à confirmer'}),
        required=True
    )

    telephone = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Téléphone'}),
        required=False
    )
    numero = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Numero de rue'}),
        required=True
    )
    rue = forms.CharField(
        label='',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Rue'}),
        required=True
    )
    codePostal = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Code postal'}),
        required=True
    )
    ville = forms.CharField(
        label='',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Ville'}),
        required=True
    )
    information = forms.CharField(
        label='',
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'control-label', 'placeholder': 'Information'}),
        required=False
    )


class ProfileForm(forms.Form):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'name'}),
        required=True,

    )
    passwd = forms.CharField(
        label='',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'}),
        required=True
    )


class ProductForm(forms.Form):
    CATCHOICE = [
        ('Fruit/Légume', 'Fruit/Légume'),
        ('Produit laitier', 'Produit laitier'),
        ('Charcuterie', 'Charcuterie'),
        ('Boisson', 'Boisson'),
        ('Divers', 'Divers')
    ]
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'nom du produit'}),
        required=True
    )
    category = forms.ChoiceField(
        choices=CATCHOICE,
        required=True
    )
    disponibility = forms.BooleanField(
        label='Disponible',
        widget=forms.NullBooleanSelect(attrs={'class': 'form-group', 'placeholder': 'disponibilité'}),
        required=True,

    )
    price = forms.DecimalField(
        label='',
        max_digits=5,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'prix'}),
    )
    picture = forms.ImageField(
        label='Image',
        widget=forms.FileInput(attrs={'class': 'form-group', 'placeholder': 'glisser une image ici'}),
        required=False
    )
    information = forms.CharField(
        label='',
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'control-label', 'placeholder': 'Information'}),
        required=False
    )


class BascketForm(forms.Form):
    quantity = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Quantité'}),
        required=True
    )


class StatusForm(forms.Form):
    CHOICE = [
        (1, 'non lus'),
        (2, 'Pris en compte'),
        (3, 'prêt'),
        (4, 'récupéré')

    ]

    status = forms.ChoiceField(
        choices=CHOICE,
        required=True
    )


class RegisterModifForm(forms.Form):
    nom = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Nom'}),
        required=False,

    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-group', 'placeholder': 'Email'}),
        required=False

    )
    passwd = forms.CharField(
        label='',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'}),
        required=False
    )
    confPasswd = forms.CharField(
        label='',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe à confirmer'}),
        required=False
    )

    telephone = forms.IntegerField(
        label=' ',
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Téléphone'}),
        required=False
    )
    numero = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Numero de rue'}),
        required=False
    )
    rue = forms.CharField(
        label='',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Rue'}),
        required=False
    )
    codePostal = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Code postal'}),
        required=False
    )
    ville = forms.CharField(
        label='',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Ville'}),
        required=False
    )
    information = forms.CharField(
        label='',
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'control-label', 'placeholder': 'Information'}),
        required=False
    )



class ProductModifForm(forms.Form):
    CATCHOICE = [
        ('Fruit/Légume', 'Fruit/Légume'),
        ('Produit laitier', 'Produit laitier'),
        ('Charcuterie', 'Charcuterie'),
        ('Boisson', 'Boisson'),
        ('Divers', 'Divers')
    ]
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'nom du produit'}),
        required=False
    )
    category = forms.ChoiceField(
        choices=CATCHOICE,
        required=True
    )
    disponibility = forms.BooleanField(
        label='Disponible',
        widget=forms.NullBooleanSelect(attrs={'class': 'form-group', 'placeholder': 'disponibilité'}),
        required=False

    )
    price = forms.DecimalField(
        label='',
        max_digits=5,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'prix'}),
    )
    picture = forms.ImageField(
        label='Image',
        widget=forms.FileInput(attrs={'class': 'form-group', 'placeholder': 'glisser une image ici'}),
        required=False
    )
    information = forms.CharField(
        label='',
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'control-label', 'placeholder': 'Information'}),
        required=False
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Rechercher un produit'}),
        required=False
    )


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])
