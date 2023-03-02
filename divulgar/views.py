from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.contrib.auth.decorators import login_required
from.models import Tag, Raca, Pet
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect
from adotar.models import PedidoAdocao
from django.views.decorators.csrf import csrf_exempt
 

@login_required
def novo_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        racas = Raca.objects.all()

        return render(request, 'novo_pet.html', {'tags': tags, 'racas': racas})
    elif request.method == "POST":
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        #validar ou incrementar

        pet = Pet(
            usuario=request.user,
            foto = foto,
            nome = nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca
        )
        pet.save()

        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)
        
        pet.save()
        return redirect('/divulgar/seus_pets')

@login_required
def seus_pets(request):
    if request.method =="GET":
        pets = Pet.objects.filter(usuario=request.user)
        return render(request, 'seus_pets.html', {'pets': pets})

def remover_pet(request, id):
    pet = Pet.objects.get(id=id)

    if not pet.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esee pet não é seu.')
        return redirect('/divulgar/seus_pets')         

    pet.delete()

    messages.add_message(request, constants.SUCCESS, 'Pet removido com sucesso')
    return redirect('/divulgar/seus_pets')

def ver_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id=id)
        return render(request, 'ver_pet.html', {'pet': pet})

def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})

def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')

@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas}

    return JsonResponse(data)