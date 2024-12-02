from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from .models import *

class RegistrarForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Usuário',
    }))

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha',
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme a Senha',
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    error_messages = {
        "password_mismatch": _("As senhas não coincidem."),
        "duplicated_username": _("Este nome de usuário já está em uso."), 
        "email_in_use": _("Este email já está em uso"),
        "password_too_similar": _("A senha é muito parecida com o nome de usuário."),
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self._meta.model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_in_use'],
                code='email_in_use',
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and self._meta.model.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                self.error_messages['duplicated_username'],
                code='duplicated_username',
            )
        return username


class PRCustomizadoForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'e-mail'}),
    )
    

class SPCustomizadoForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova Senha'}),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Nova Senha'}),
    )


class AddImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        exclude = ['user']
        error_messages = {
            'imagem': {
                'invalid_image': _("O arquivo carregado não é uma imagem válida. Por favor, escolha um arquivo de imagem."),
            }
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Add custom attributes to the 'imagem' field
        self.fields['imagem'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Escolha uma imagem...',
            'accept': 'image/*', 
        })
        
        for field in self.fields.values():
            if field != self.fields['imagem']:  
                field.widget.attrs.update({'class': 'form-control mb-3'})
        
        # Filtra categorias pelo usuário
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(user=user)


class AddCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})