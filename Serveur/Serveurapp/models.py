from django.db import models

# Create your models here.
from django.db import models

class TypeServeur(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.type
    #class Meta:
        #db_table="TypeServeur"


class Serveur(models.Model):
    nom = models.CharField(max_length=50)
    type_serveur = models.ForeignKey(TypeServeur, on_delete=models.CASCADE)
    nombre_processeur = models.IntegerField()
    capacite_memoire = models.IntegerField()
    capacite_stockage = models.IntegerField()

    def __str__(self):
        return self.nom
    #class Meta:
     #   db_table="Serveur"

        

class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    #class Meta:
     #   db_table="Utilisateur"

class Service(models.Model):
    nom_service = models.CharField(max_length=50)
    date_lancement = models.DateField()
    espace_memoire_utilise = models.IntegerField()
    memoire_vive_necessaire = models.IntegerField()
    serveur_lancement = models.ForeignKey(Serveur, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_service
    #class Meta:
    #    db_table="Service"

class Application(models.Model):
    nom_application = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos/')
    services = models.ManyToManyField(Service)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_application
    #class Meta:
     #   db_table="Application"


