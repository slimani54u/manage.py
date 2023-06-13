from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datetime_safe import datetime
from django.views import View
from django.contrib import messages
import os
from django.conf import settings
from .forms import ApplicationFileForm
from .models import Serveur, TypeServeur, Utilisateur, Service, Application
from .forms import ServeurForm, TypeServeurForm, UtilisateurForm, ServiceForm, ApplicationForm
from django.http import HttpResponse, HttpResponseRedirect


from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Serveur, Service
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
    return render(request, 'Serveurapp/Utilisateur/utilisateur_update.html', {'form': form,'utilisateur':utilisateur})

def utilisateur_delete(request, pk):
    utilisateur = Utilisateur.objects.get(pk=pk)
    utilisateur.delete()
    HttpResponseRedirect("/")


# Vues CRUD pour le modèle Service
from django.db.models import F


def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)

            if service.espace_memoire_utilise > service.serveur_lancement.capacite_stockage:
                error_message = "La capacité de stockage du serveur est insuffisante pour ce service."
                return render(request, 'Serveurapp/Services/service_create.html',
                              {'form': form, 'error_message': error_message})

            if service.memoire_vive_necessaire > service.serveur_lancement.capacite_memoire:
                error_message = "La capacité mémoire du serveur est insuffisante pour ce service."
                return render(request, 'Serveurapp/Services/service_create.html',
                              {'form': form, 'error_message': error_message})
            service.save()
            service.serveur_lancement.capacite_stockage = service.serveur_lancement.capacite_stockage - service.espace_memoire_utilise
            service.serveur_lancement.capacite_memoire = service.serveur_lancement.capacite_memoire - service.memoire_vive_necessaire
            service.serveur_lancement.save()

            return redirect('/')
    else:
        form = ServiceForm()
    return render(request, 'Serveurapp/Services/service_create.html', {'form': form})


from django.db.models import F


def service_update(request, pk):
    service = Service.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            updated_service = form.save(commit=False)
            serveur_lancement = updated_service.serveur_lancement

            # Vérifier si les capacités du service sont supérieures aux valeurs précédentes
            if (updated_service.espace_memoire_utilise >= service.espace_memoire_utilise) and (updated_service.memoire_vive_necessaire >= service.memoire_vive_necessaire):
                # Calculer les différences de mémoire et d'espace mémoire
                diff_memoire = updated_service.memoire_vive_necessaire - service.memoire_vive_necessaire
                diff_espace_memoire = updated_service.espace_memoire_utilise - service.espace_memoire_utilise

                # Vérifier si les nouvelles valeurs sont compatibles avec le serveur
                if (serveur_lancement.capacite_stockage - diff_espace_memoire >= 0) and (serveur_lancement.capacite_memoire - diff_memoire >= 0):
                    # Mettre à jour les capacités du serveur
                    serveur_lancement.capacite_stockage -= diff_espace_memoire
                    serveur_lancement.capacite_memoire -= diff_memoire

                    # Mettre à jour le service avec les nouvelles valeurs
                    updated_service.save()
                    serveur_lancement.save()
                    return redirect('/')
                else:
                    # Capacité insuffisante du serveur, afficher un message d'erreur approprié
                    error_message = "La capacité du serveur est insuffisante pour les nouvelles valeurs."
                    return render(request, 'Serveurapp/Services/service_update.html', {'form': form, 'service': service, 'error_message': error_message})
            else:
                # Capacités inférieures aux valeurs précédentes, mettre à jour les capacités du serveur
                diff_capacite_stockage = service.espace_memoire_utilise - updated_service.espace_memoire_utilise
                diff_capacite_memoire = service.memoire_vive_necessaire - updated_service.memoire_vive_necessaire

                # Vérifier si les nouvelles valeurs sont compatibles avec le serveur
                if (serveur_lancement.capacite_stockage + diff_capacite_stockage >= 0) and (serveur_lancement.capacite_memoire + diff_capacite_memoire >= 0):
                    # Mettre à jour les capacités du serveur
                    serveur_lancement.capacite_stockage += diff_capacite_stockage
                    serveur_lancement.capacite_memoire += diff_capacite_memoire

                    # Mettre à jour le service avec les nouvelles valeurs
                    updated_service.save()
                    serveur_lancement.save()
                    return redirect('/')
                else:
                    # Capacité insuffisante du serveur, afficher un message d'erreur approprié
                    error_message = "La capacité du serveur est insuffisante pour les nouvelles valeurs."
                    return render(request, 'Serveurapp/Services/service_update.html', {'form': form, 'service': service, 'error_message': error_message})
    else:
        form = ServiceForm(instance=service)
    return render(request, 'Serveurapp/Services/service_update.html', {'form': form, 'service': service})




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

from .models import Application, Service

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.core.files.base import ContentFile


def process_uploaded_file(file):
    content = file.read().decode('utf-8')
    lines = content.split('\n')

    application_name = lines[0].strip()
    service_infos = [line.strip().split(',') for line in lines[1:] if line.strip()]

    utilisateur = Utilisateur.objects.get(pk=1)  # Remplacez 1 par l'ID de l'utilisateur approprié
    serveur = Serveur.objects.get(pk=2)  # Remplacez 2 par l'ID du serveur de déploiement approprié

    application = Application(nom_application=application_name, utilisateur=utilisateur)
    application.save()

    for info in service_infos:
        service_name, date_lancement, espace_memoire, memoire_vive = info

        service = Service.objects.create(
            nom_service=service_name,
            date_lancement=date_lancement,
            espace_memoire_utilise=espace_memoire,
            memoire_vive_necessaire=memoire_vive,
            serveur_lancement=serveur
        )
        service.save()
        application.services.add(service)


def upload_application(request):
    if request.method == 'POST':
        form = ApplicationFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Récupérer le fichier
            uploaded_file = request.FILES['file']

            # Analyser le fichier pour insérer l'application et les services associés
            process_uploaded_file(uploaded_file)

            # Redirection vers une page de confirmation ou autre
            return HttpResponseRedirect('/')  # Remplacez "/success/" par l'URL de votre choix
    else:
        form = ApplicationFileForm()
    return render(request, 'Serveurapp/upload_application.html', {'form': form})

from django.http import HttpResponse

from django.shortcuts import redirect

from django.urls import reverse


def generate_service_report(request):
    if request.method == 'POST':
        serveur_id = request.POST.get('serveur_id')
        try:
            serveur = Serveur.objects.get(id=int(serveur_id))
            services = Service.objects.filter(serveur_lancement=serveur)

            # Générer le contenu de la fiche des services
            content = "Fiche des services lancés sur le serveur {}\n\n".format(serveur.nom)
            for service in services:
                content += "Service : {}\n".format(service.nom_service)
                content += "Date de lancement : {}\n".format(service.date_lancement)
                content += "Espace mémoire utilisé : {}\n".format(service.espace_memoire_utilise)
                content += "Mémoire vive nécessaire : {}\n\n".format(service.memoire_vive_necessaire)

            # Créer une réponse HTTP avec le contenu de la fiche des services
            response = HttpResponse(content, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="fiche_services.txt"'

            # Retourner la réponse HTTP pour déclencher le téléchargement
            return response
        except Serveur.DoesNotExist:
            return HttpResponse('Serveur non trouvé.')
    else:
        return render(request, 'Serveurapp/generate_service_report.html')

