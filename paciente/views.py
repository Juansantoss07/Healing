from django.shortcuts import render
from medico.models import DadosMedico, Especialidades

# Create your views here.
def home(request):
    medicos = DadosMedico.objects.all()
    especialidades = Especialidades.objects.all()

    medicos_filtrar = request.GET.get('medico')
    especialidades_filtrar = request.GET.getlist('especialidades')

    if medicos_filtrar:
        medicos = medicos.filter(nome__icontains=medicos_filtrar)

    if especialidades_filtrar:
       medicos = medicos.filter(especialidades_id__in=especialidades_filtrar)

    return render(request, 'home.html', {'medicos':medicos, 'especialidades': especialidades})