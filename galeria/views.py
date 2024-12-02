from django.contrib.auth.mixins import LoginRequiredMixin as lr
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import * 
from .models import *

# Create your views here.
class RegistrarView(CreateView):
    template_name = 'registrar.html'
    form_class = RegistrarForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('galeria')


class Galeria(lr, ListView):
    template_name = 'galeria.html'
    
    def get_queryset(self):
        categoria_id = self.request.GET.get('categoria')
        
        if categoria_id:
            self.categoria = get_object_or_404(Categoria, id=categoria_id, user=self.request.user)
            return Imagem.objects.filter(categoria=self.categoria, user=self.request.user)
        else:
            self.categoria = None
            return Imagem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_filtro'] = getattr(self, 'categoria', None)
        return context 


class Deslogar(lr, TemplateView):
    template_name = 'deslogar.html'


class AdicionarImagem(lr, CreateView):
    template_name = 'adicionar_imagem.html'
    model = Imagem
    form_class = AddImagemForm
    success_url = reverse_lazy('galeria')
    
    def form_valid(self, form):
        # Associa a imagem com o usuário atual
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Passa o usuário para filtrar categorias
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AdicionarCategoria(lr, CreateView):
    template_name = 'adicionar_categoria.html'
    model = Categoria
    form_class = AddCategoriaForm
    success_url = reverse_lazy('addImagem')

    def form_valid(self, form):
        # Define o usuário atual como o usuário que criou a categoria
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class VerImagem(lr, DetailView):
    template_name = 'detalhes.html'
    model = Imagem


class ApagarImagem(lr, DeleteView):
    template_name = 'apagar_imagem.html'
    model = Imagem
    success_url = reverse_lazy('galeria')
