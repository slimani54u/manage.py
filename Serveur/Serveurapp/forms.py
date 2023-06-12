from django import forms
from .models import Serveur, TypeServeur, Utilisateur, Service, Application

class ServeurForm(forms.ModelForm):
    class Meta:
        model = Serveur
        fields = '__all__'  # Utilisez les champs que vous souhaitez afficher dans le formulaire


class TypeServeurForm(forms.ModelForm):
    class Meta:
        model = TypeServeur
        fields = '__all__'


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class ApplicationForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all())

    class Meta:
        model = Application
        fields = '__all__'
