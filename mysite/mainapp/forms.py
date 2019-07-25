from django import forms


class ContactForm (forms.Form):
    name = forms.CharField(label='Имя', max_length=30)
    phone = forms.CharField(label='Номер телефона', max_length=30)
    email = forms.EmailField(label='Email', max_length=254)
    message = forms.CharField(label='', max_length=2000, widget=forms.Textarea, required=True)