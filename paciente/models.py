from django.db import models
from django.contrib.auth.models import User
from medico.models import DatasAbertas

# Create your models here.
class Consulta(models.Model):

    status_choices = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada'),
    )

    paciente = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_aberta = models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.paciente.username
    
class Documentos(models.Model):
    titulo = models.CharField(max_length=100)
    documento = models.FileField(upload_to='documentos')
    consulta = models.ForeignKey(Consulta, on_delete=models.DO_NOTHING)

    def __str__(self):  
        return self.titulo