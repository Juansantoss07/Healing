from django.shortcuts import render, redirect
from . models import DadosMedico, Especialidades, is_medico, DatasAbertas
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def cadastro_medico(request):

    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você já é médico(a)')
        return redirect('/medicos/abrir_horario')

    if request.method == 'GET':
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades': especialidades})
    
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
    return redirect('/medicos/abrir_horarios')

def abrir_horario(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você não é médico(a)')
        return redirect('/usuarios/logout')
    
    if request.method == "GET":
        dadosMedico = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'abrir_horario.html', {'dadosMedico': dadosMedico, 'datas_abertas': datas_abertas})
    
    elif request.method == "POST":
        data = request.POST.get('data')
        
        dataFormatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        dataAtual = datetime.now()
        
        if dataFormatada <= dataAtual:
            messages.add_message(request, constants.ERROR, 'Ops...Não tem como agendar para uma data que já passou! Escolha outra data.')
            return redirect('/medicos/abrir_horario')
        
        datasAbertas = DatasAbertas(
            data=data,
            user=request.user
        )

        datasAbertas.save()
        messages.add_message(request, constants.SUCCESS, 'Horário aberto com sucesso!')
        return redirect('/medicos/abrir_horario')