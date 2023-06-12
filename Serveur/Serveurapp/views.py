from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
import os
from django.conf import settings

from .models import Serveur, TypeServeur, Utilisateur, Service, Application
from .forms import ServeurForm, TypeServeurForm, UtilisateurForm, ServiceForm, ApplicationForm
# Create your views here.


def base_view(request):
    typeserveurs = TypeServeur.objects.all()
    serveurs = Serveur.objects.all()
    utilisateurs = Utilisateur.objects.all()
    applications = Application.objects.all()
    services= Service.objects.all()

    context = {
        'typeserveurs': typeserveurs,
        'serveurs': serveurs,
        'utilisateurs': utilisateurs,
        'applications': applications,
        'services': services
    }

    return render(request, 'Serveurapp/base.html', context)
# Vues CRUD pour le modèle TypeServeur
def typeserveur_create(request):
    if request.method == 'POST':
        form = TypeServeurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TypeServeurForm()
    return render(request, 'Serveurapp/typeServeur/typeserveur_create.html', {'form': form})


def typeserveur_update(request, pk):
    typeserveur = TypeServeur.objects.get(pk=pk)
    if request.method == 'POST':
        form = TypeServeurForm(request.POST, instance=typeserveur)
        if form.is_valid():
            form.save()
            return redirect('typeserveur_list')


def typeserveur_delete(request, pk):
    typeserveur = TypeServeur.objects.get(pk=pk)

    typeserveur.delete()
    HttpResponseRedirect("/")

def serveur_create(request):
    if request.method == 'POST':
        form = ServeurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ServeurForm()
    return render(request, 'Serveurapp/Serveur/serveur_create.html', {'form': form})


def serveur_update(request, pk):
    serveur = Serveur.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServeurForm(request.POST, instance=serveur)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ServeurForm(instance=serveur)
    return render(request, 'Serveurapp/Serveur/serveur_update.html', {'form': form, 'serveur': serveur})






def serveur_delete(request, pk):
    serveur = Serveur.objects.get(pk=pk)
    serveur.delete()
    return HttpResponseRedirect("/")


# Vues CRUD pour le modèle Utilisateur
def utilisateur_create(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UtilisateurForm()
    return render(request, 'Serveurapp/Utilisateur/utilisateur_create.html', {'form': form})

def utilisateur_update(request, pk):
    utilisateur = Utilisateur.objects.get(pk=pk)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, instance=utilisateur)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UtilisateurForm(instance=utilisateur)
    return render(request, 'Serveurapp/utilisateur_update.html', {'form': form})

def utilisateur_delete(request, pk):
    utilisateur = Utilisateur.objects.get(pk=pk)
    utilisateur.delete()
    HttpResponseRedirect("/")


# Vues CRUD pour le modèle Service
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)

            service.save()
            return redirect('/')
    else:
        form = ServiceForm()
    return render(request, 'Serveurapp/Services/service_create.html', {'form': form})

def service_update(request, pk):
    service = Service.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'Serveurapp/Services/service_update.html', {'form': form,'service':service})

def service_delete(request, pk):
    service = Service.objects.get(pk=pk)
    service.delete()
    return HttpResponseRedirect("/")


# Vues CRUD pour le modèle Application
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()

            messages.success(request, 'L\'application a été créée avec succès.')
            return redirect('/')
    else:
        form = ApplicationForm()
    return render(request, 'Serveurapp/Application/application_create.html', {'form': form})

def application_update(request, pk):
    application = Application.objects.get(pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.save()
            messages.success(request, 'L\'application a été mise à jour avec succès.')
            return redirect('/')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'Serveurapp/Application/application_update.html', {'form': form,'app':application})


def application_delete(request, pk):
    application = Application.objects.get(pk=pk)

    # Récupérer le chemin complet de l'image
    image_path = os.path.join(settings.MEDIA_ROOT, str(application.logo))

    # Supprimer l'instance d'Application
    application.delete()

    # Supprimer l'image du dossier
    if os.path.exists(image_path):
        os.remove(image_path)

    return HttpResponseRedirect("/")

