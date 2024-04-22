from django.shortcuts import render, redirect
from medico.models import DadosMedico, Especialidades, DatasAbertas, is_medico
from django.contrib.auth.models import User
from datetime import datetime
from django.http import HttpResponse
from .models import Consulta, Documentos
from django.contrib import messages
from django.contrib.messages import constants

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

    return render(request, 'home.html', {'medicos':medicos, 'especialidades': especialidades, 'is_medico':is_medico(request.user)})

def escolher_horario(request, id_dados_medico):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id = id_dados_medico)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False).order_by('data')
    
        
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico':is_medico(request.user)})
    

def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id = id_data_aberta)

        consultaMarcada = Consulta(
            paciente = request.user,
            data_aberta = data_aberta
        )

        consultaMarcada.save()

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Consulta agendada com sucesso!')
        return redirect('/paciente/minhas_consultas')


def minhas_consultas(request):
    if request.method == "GET":
        consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())

        filtro_consultas = request.GET.get('nome')
        filtros_consultas_data = request.GET.get('data')
        if filtro_consultas:
            consultas = consultas.filter(data_aberta__user__username__icontains=filtro_consultas)
        if filtros_consultas_data:
            consultas = consultas.filter(data_aberta__data__icontains=filtros_consultas_data)
    return render(request, 'minhas_consultas.html', {'consultas':consultas, 'is_medico':is_medico(request.user)})

def consulta(request, id_consulta):
    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        documentos = Documentos.objects.filter(consulta__id=id_consulta)
        return render(request, 'consulta.html', {'consulta':consulta, 'dado_medico':dado_medico, 'is_medico':is_medico(request.user), 'documentos':documentos})
    

def cancela_consulta(request, id_consulta):
    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)

        if request.user != consulta.paciente:
            messages.add_message(request, constants.WARNING, 'Não é possível cancelar uma consulta que não é sua.')
            return redirect('/paciente/consulta/' + str(id_consulta))
        
        consulta.status = "C"
        consulta.save()

        messages.add_message(request, constants.SUCCESS, 'Consulta cancelada com sucesso!')
        return redirect('/paciente/consulta/' + str(id_consulta))   
    

def envia_documentos(request, id_consulta):
    if not is_medico:
        messages.add_message(request, constants.WARNING, 'Você não é médico(a)')
        return redirect('/paciente/home')
    
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')
    consulta = Consulta.objects.get(id=id_consulta)

    documentos = Documentos(
        titulo=titulo,
        documento=documento,
        consulta_id=consulta.id
    )

    documentos.save()
    messages.add_message(request, constants.SUCCESS, 'Documento(s) adicionado(s) com sucesso!')
    return redirect('/medico/consulta_area_medico/' + str(consulta.id))
