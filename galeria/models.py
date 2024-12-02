from django.db import models
from django.conf import settings
from google.cloud import storage

# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#referencing-the-user-model 
class Categoria(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)  # Chave estrangeira p/ usuário

    def __str__(self):
        return self.nome
    
class Imagem(models.Model):
    imagem = models.ImageField(upload_to='', null=False, blank=False)
    descricao = models.TextField(blank=False, null=False, verbose_name='descrição')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)  # Chave estrangeira p/ usuário
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Deleta a foto do bucket do GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(settings.BUCKET)

        # Usa o caminho completo, considerando a 'location'
        blob_path = f"{settings.STORAGES['default']['OPTIONS']['location']}{self.imagem.name}"
        blob = bucket.blob(blob_path)
        blob.delete()

        # Deleta as informações do banco de dados
        super().delete(*args, **kwargs)