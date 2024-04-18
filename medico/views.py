from django.shortcuts import render

# Create your views here.
def cadastro_medico(request):
    if request.method == 'GET':
        return render(request, 'cadastro_medico.html')