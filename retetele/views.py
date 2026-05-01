import os

from django.http.request import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden


from retetele.forms import ReteteForm, CommentForm
from retetele.models import Retete, Like

from prieteni.models import CustomUser

def lista_retete(request: HttpRequest):
    sort = request.GET.get("sort", "-data_creare")

    valid_sort = ["nume", "-nume", "data_creare", "-data_creare"]
    if sort not in valid_sort:
        sort = "-data_creare"

    retete = Retete.objects.all().order_by(sort)

    categorie = request.GET.get("categorie")

    if categorie:
        retete = retete.filter(categorie=categorie)

    paginator = Paginator(retete, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "retetele/home.html", {"page_obj": page_obj})



@login_required
def introducere_reteta(request: HttpRequest):
    if request.method == 'POST':
        form = ReteteForm(request.POST)
        if form.is_valid():
            retete = form.save(commit=False)
            retete.user = request.user
            retete.save()
            return redirect('retete')
    else:
        form = ReteteForm()
    context = {'form': form}
    return render(request, 'retetele/formular_retete.html', context)

def stergere_reteta(request: HttpRequest, pk: int):
    reteta = get_object_or_404(Retete, pk=pk)
    if request.method == "POST":
        reteta.delete()
        return redirect('retete')
    else:
        return render(request, 'retetele/confirmare_steregere.html', {'retete': reteta})

def modificare_reteta(request: HttpRequest, pk: int):
    reteta = get_object_or_404(Retete, pk=pk)
    if reteta.user != request.user:
        return HttpResponseForbidden("Aceasta nu este reteta ta, nu ai voie sa modifici!")
    if request.method == "POST":
        form = ReteteForm(request.POST, instance=reteta)
        if form.is_valid():
            form.save()
            return redirect('retete')
    else:
        form = ReteteForm(instance=reteta)
    return render(request, 'retetele/formular_retete.html', {'form': form})

def retetele_prietenilor (request: HttpRequest, pk: int):
    user = get_object_or_404(CustomUser, pk=pk)
    retete = user.retete.all().order_by("-pk")
    paginator = Paginator(retete, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "retetele/home.html", context)

def cautare_retete(request):
    q = request.GET.get("q", "")
    categorie = request.GET.get("categorie", "")

    retete = Retete.objects.all()

    if q:
        retete = retete.filter(nume__icontains=q)

    if categorie:
        retete = retete.filter(categorie=categorie)

    paginator = Paginator(retete.order_by("-data_creare"), 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    querystring = f"&q={q}&categorie={categorie}"

    return render(request, "retetele/home.html", {
        "page_obj": page_obj,
        "querystring": querystring
    })

def adauga_poza(request: HttpRequest, pk: int):
    reteta = get_object_or_404(Retete, pk=pk)
    print("METHOD:", request.method)
    print("FILES:", request.FILES)
    if request.method == "POST" and request.FILES.get("poza"):
        reteta.poza = request.FILES["poza"]
        reteta.save()
        return redirect("retete")
    return redirect("retete")

def sterge_poza(request: HttpRequest, pk: int):
    reteta = get_object_or_404(Retete, pk=pk)

    if request.method == "POST":
        if reteta.poza:
            if os.path.isfile(reteta.poza.path):
                os.remove(reteta.poza.path)

            reteta.poza = None
            reteta.save()

    return redirect("retete")

@login_required
def adauga_comment(request, pk):
    reteta = get_object_or_404(Retete, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.reteta = reteta
            comment.user = request.user
            comment.save()


    return redirect(request.META.get("HTTP_REFERER", "retete"))

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Retete, Like

@login_required
def adauga_like(request, pk):
    reteta = get_object_or_404(Retete, pk=pk)

    like, created = Like.objects.get_or_create(
        reteta=reteta,
        user=request.user
    )

    if not created:
        like.delete()

    page = request.GET.get("page")

    if page:
        return HttpResponseRedirect(f"/?page={page}")

    return redirect("retete")



