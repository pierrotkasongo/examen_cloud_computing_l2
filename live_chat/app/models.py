from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField

class Promotion(models.Model):
    uid = ShortUUIDField(unique=True, length=20, max_length=20)
    name = models.CharField(max_length=100, unique=True)
    date_create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    uid = ShortUUIDField(unique=True, length=20, max_length=20)
    username = models.CharField(max_length=50, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50) 
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["username","status"] 
    def __str__(self):
        return self.username

class Etudiant(models.Model):
    uid = ShortUUIDField(unique=True, length=20, max_length=20)
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    promotionId = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    number_matricule = models.CharField(max_length=50, unique=True)
    number_phone = models.CharField(max_length=20, blank=True, null=True)
    date_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    date_create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Message(models.Model):
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message de {self.expediteur.username} à {self.destinateur.username}"