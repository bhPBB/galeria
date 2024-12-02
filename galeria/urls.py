from django.contrib.auth.views import PasswordResetView as PR, PasswordResetConfirmView as PRC
from .forms import PRCustomizadoForm, SPCustomizadoForm
from django.urls import path
from .views import *

urlpatterns = [
    path('', Galeria.as_view(), name='galeria', kwargs={'categoria': None}),
    path('registrar/', RegistrarView.as_view(), name='registrar'),
    path('sair/', Deslogar.as_view(), name='sair'),
    path('nova_imagem/', AdicionarImagem.as_view(), name='addImagem'),
    path('nova_categoria/', AdicionarCategoria.as_view(), name='addCategoria'),
    path('trocar-senha/', PR.as_view(form_class=PRCustomizadoForm), name='password_reset'),
    path('trocar-senha/<uidb64>/<token>/', PRC.as_view(form_class=SPCustomizadoForm), name='password_reset_confirm'),
    path('imagem/<int:pk>/', VerImagem.as_view(), name='verImagem'),
    path('imagem/<int:pk>/apagar', ApagarImagem.as_view(), name='apagarImagem'),
]