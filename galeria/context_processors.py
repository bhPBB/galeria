from .models import Categoria

def categorias(request):
    if request.user.is_authenticated:
        categorias = Categoria.objects.filter(user=request.user)
    else:
        categorias = Categoria.objects.none() 
    return {
        'categorias': categorias
    }