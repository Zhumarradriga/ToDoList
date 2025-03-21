from django import forms
from .models import CustomUser


class CustomRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    phone_number = forms.CharField(max_length=15, required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'Телефон'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ' Подтвердите пароль'}))

    def clean_email(self):
        email = self.cleaned_data['data']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email

    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        password_confirm = clean_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return clean_data


class CustomLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
