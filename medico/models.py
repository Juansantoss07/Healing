from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Especialidades(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class DadosMedico(models.Model):
    crm = models.CharField(max_length=13)
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length = 15)
    rua = models.CharField(max_length = 100)
    bairro = models.CharField(max_length = 100)
    numero = models.IntegerField()
    rg = models.ImageField(upload_to='rgs')
    cedula_identidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to='fotos_perfil')
    descricao = models.TextField()
    valor_consulta = models.FloatField(default=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    especialidades = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username