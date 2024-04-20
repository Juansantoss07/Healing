from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmaSenha = request.POST['confirmar_senha']
        
        if senha != confirmaSenha:
            messages.add_message(request, constants.ERROR, 'A senha deve ser idêntica ao confirmar senha.')
            return redirect('/usuarios/cadastro')
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve conter ao menos 6 digitos.')
            return redirect('/usuarios/cadastro')
        
        users = User.objects.filter(username = username)
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse username.')
            return redirect('/usuarios/cadastro')
        
        user = User.objects.create_user(
            username= username,
            email= email,
            password= senha
        )
        
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
        return redirect('/usuarios/login')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            return redirect('/paciente/home')
        
        messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
        return redirect('/usuarios/login')
    

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')