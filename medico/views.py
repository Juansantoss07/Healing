from django.shortcuts import render, redirect
from . models import DadosMedico, Especialidades, is_medico
from django.contrib import messages
from django.contrib.messages import constants

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