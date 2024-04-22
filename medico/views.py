from django.shortcuts import render, redirect
from . models import DadosMedico, Especialidades, is_medico, DatasAbertas
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from datetime import datetime, timedelta
from paciente.models import Consulta, Documentos


# Create your views here.
def cadastro_medico(request):

    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você já é médico(a)')
        return redirect('/medico/abrir_horario')

    if request.method == 'GET':
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades': especialidades, 'is_medico':is_medico(request.user)})
    
    elif request.method == 'POST':
        crm = request.POST.get('crm')
        cim = request.FILES.get('cim')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialide =request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')
        user = request.user
        especialidades = Especialidades.objects.get(nome=especialide)

    DadosMedico.objects.create(crm=crm, nome=nome, cep=cep, rua=rua, bairro=bairro, numero=numero, rg=rg, cedula_identidade_medica=cim, foto=foto, descricao=descricao, valor_consulta=valor_consulta, user=user, especialidades=especialidades)

    messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso')
    return redirect('/medico/abrir_horarios')

def abrir_horario(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você não é médico(a)')
        return redirect('/usuarios/logout')
    
    if request.method == "GET":
        dadosMedico = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'abrir_horario.html', {'dadosMedico': dadosMedico, 'datas_abertas': datas_abertas,'is_medico':is_medico(request.user)})
    
    elif request.method == "POST":
        data = request.POST.get('data')
        
        dataFormatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        dataAtual = datetime.now()
        
        if dataFormatada <= dataAtual:
            messages.add_message(request, constants.ERROR, 'Ops...Não tem como agendar para uma data que já passou! Escolha outra data.')
            return redirect('/medico/abrir_horario')
        
        datasAbertas = DatasAbertas(
            data=data,
            user=request.user
        )

        datasAbertas.save()
        messages.add_message(request, constants.SUCCESS, 'Horário aberto com sucesso!')
        return redirect('/medico/abrir_horario')
    
def consultas_medico(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você não é médico(a)')
        return redirect('/usuarios/logout')
    
    if request.method == "GET":
        hoje = datetime.now()

        consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
        consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id')).filter(data_aberta__user=request.user)

        filtro_consultas = request.GET.get('nome')
        filtro_consultas_data = request.GET.get('data')
        if filtro_consultas:
            consultas_hoje = consultas_hoje.filter(paciente__username__icontains=filtro_consultas)
            consultas_restantes = consultas_restantes.filter(paciente__username__icontains=filtro_consultas)
        if filtro_consultas_data:
            consultas_hoje = consultas_hoje.filter(data_aberta__data__icontains= filtro_consultas_data)
            consultas_restantes = consultas_restantes.filter(data_aberta__data__icontains=filtro_consultas_data)
        return render(request, 'consultas_medico.html', {'consultas_hoje':consultas_hoje, 'consultas_restantes':consultas_restantes, 'is_medico':is_medico(request.user)})
    

def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você não é médico(a)')
        return redirect('/usuarios/logout')
    
    documentos = Documentos.objects.filter(consulta__id=id_consulta)
    
    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        return render(request, 'consulta_area_medico.html', {'is_medico':is_medico(request.user), 'consulta':consulta, 'documentos':documentos   })
    
    elif request.method == "POST":
        consulta = Consulta.objects.get(id=id_consulta)
        consulta_link = request.POST.get('link')

        if(consulta.status == "C"):
            messages.add_message(request, constants.ERROR, 'Não é possível iniciar uma consulta cancelada!')
            return redirect('/medico/consulta_area_medico/' + str(consulta.id))
        elif(consulta.status == "F"):
            messages.add_message(request, constants.ERROR, 'Não é possível iniciar uma consulta finalizada!')
            return redirect('/medico/consulta_area_medico/' + str(consulta.id))
        
        consulta.link = consulta_link
        consulta.status = "I"
        consulta.save()

        messages.add_message(request, constants.SUCCESS, 'Link salvo e consulta iniciada!')
        return redirect('/medico/consulta_area_medico/' + str(consulta.id))


def finalizar_consulta(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você não é médico(a)')
        return redirect('/usuarios/logout')

    consulta = Consulta.objects.get(id=id_consulta)

    if(request.user != consulta.data_aberta.user):
        messages.add_message(request, constants.ERROR, 'Não é possível finalizar uma consulta de outro médico!')
        return redirect('/medico/consulta_area_medico/' + str(consulta.id))

    if(consulta.status == "C"):
        messages.add_message(request, constants.ERROR, 'Não é possível finalizar uma consulta cancelada!')
        return redirect('/medico/consulta_area_medico/' + str(consulta.id))
    elif(consulta.status == "F"):
        messages.add_message(request, constants.ERROR, 'Não é possível finalizar uma consulta já finalizada!')
        return redirect('/medico/consulta_area_medico/' + str(consulta.id))
    
    consulta.status = "F"
    consulta.save()
    return redirect('/medico/consulta_area_medico/' + str(consulta.id))