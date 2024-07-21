from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.views import View
from django.contrib import messages
from live_chat import settings
from django.core.mail import send_mail
from .models import *
from datetime import datetime, timedelta
from .password_generator import generate_password
import random
import string

# Create your views here.
class Connect(View):
    def get(self, request):
        template_name = "app_auth/connect.html"
        title = "Connexion"
        return render(request, template_name, {'title':title})
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if user.status == 'admin':
                return redirect('dashboardAdmin')
            elif user.status == 'etudiant':
                return redirect('chatEtudiant')
        else:
            messages.error(request, "Informations incorrectes")
            return redirect('connect')

class DashboardAdmin(View):
    def get(self, request):
        if request.user.is_authenticated: 
            template_name = "app/admin/dashboard.html"
            title = "Tableau de bord"
            now = datetime.today().strftime('%A %d %B %Y, %H:%M')
            promotion_count = Promotion.objects.count()
            etudiant_count = Etudiant.objects.count()
        return render(request, template_name, {'title':title, 'now':now, 'promotion_count':promotion_count, 'etudiant_count':etudiant_count})

class AjoutEtudiantAdmin(View): 
    def get(self, request):
        if request.user.is_authenticated:
            template_name = "app/admin/ajoute_etudiant.html"
            title = "Ajout Etudiant"
            now = datetime.today().strftime('%A %d %B %Y, %H:%M')
            promotions = Promotion.objects.all()
            etudiants = Etudiant.objects.all()
            return render(request, template_name, {'title':title, 'now':now, 'etudiants':etudiants,'promotions':promotions})
    def post(self, request):
        if request.user.is_authenticated:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            random_number= ''.join(random.choices(string.digits, k=12))
            number_matricule = f"ETUDIANT-{random_number}"
            date_birth = request.POST.get('date_birth')
            sex = request.POST.get('sex')
            number_phone = request.POST.get('number_phone')
            email = request.POST.get('email') 
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email existe déjà !")
                return redirect("ajoutEtudiantAdmin")
            address = request.POST.get('address')
            promotion_uid = request.POST.get('promotion')
            get_promotion = Promotion.objects.get(uid=promotion_uid)
            password = generate_password()
            print("Mot de passe générer: ", password)
            if Etudiant.objects.filter(number_matricule=number_matricule).exists():
                messages.error(request, "Le numero matricule existe déjà !")
                return redirect("ajoutEtudiantAdmin")
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, status="etudiant")
            Etudiant.objects.create(userId=user, promotionId=get_promotion, number_matricule=number_matricule, number_phone=number_phone, date_birth=date_birth, sex=sex, address=address)
            subject = "Bienvenue dans Live-Chat Student"
            message = (f"Bonjour {first_name} {last_name},\n\n"
                       f"Voici vos informations :\n"
                       f"Nom d'utilisateur : {username}\n"
                       f"Numéro matricule : {number_matricule}\n"
                       f"Mot de passe : {password}\n\n"
                       f"Veuillez garder ces informations confidentielles.\n")
            sender = settings.EMAIL_HOST_USER
            recipient = [email]
            send_mail(subject, message, sender, recipient, fail_silently=True)
            messages.success(request, "L'enregistrement réussi")
            return redirect("ajoutEtudiantAdmin")

class UpdateEtudiantAdmin(View):
    def get(self, request, uid):
        if request.user.is_authenticated:
            title = "Modification Etudiant"
            now = datetime.today().strftime('%A %d %B %Y, %H:%M')
            try:
                item = Etudiant.objects.get(uid=uid)
            except Etudiant.DoesNotExist:
                messages.error(request, "Etudiant n'existe pas !")
                return redirect("ajoutEtudiantAdmin")
            promotions = Promotion.objects.all()
            return render(request, "app/admin/update_etudiant.html", {'title': title, 'now': now, 'item': item, 'promotions': promotions })
    def post(self, request, uid):
        if request.user.is_authenticated:
            try:
                item = Etudiant.objects.get(uid=uid)
            except Etudiant.DoesNotExist:
                messages.error(request, "L'agent n'existe pas !")
                return redirect("ajoutEtudiantAdmin")
            item.userId.username = request.POST.get('username')
            item.userId.first_name = request.POST.get('first_name')
            item.userId.last_name = request.POST.get('last_name')
            item.number_phone = request.POST.get('number_phone')
            item.userId.email = request.POST.get('email')
            item.sex = request.POST.get('sex')
            item.date_birth = request.POST.get('date_birth')
            item.address = request.POST.get('address')
            try:
                item.promotions = Promotion.objects.get(uid=request.POST.get('promotion'))
            except Promotion.DoesNotExist:
                messages.error(request, "Choisissez une promotion !")
                return redirect("ajoutEtudiantAdmin")
            item.userId.save()
            item.save()
            messages.success(request, "Modification réussi")
            return redirect("ajoutEtudiantAdmin")

class DeleteEtudiantAdmin(View):
    def get(self, request, uid):
        if request.user.is_authenticated:
            try:
                item = Etudiant.objects.get(uid=uid)
                item.userId.delete()
                messages.success(request, "Etudiant a été supprimé avec succès.")
            except Etudiant.DoesNotExist:
                messages.error(request, "Etudiant n'a pas pu être supprimé. Il n'existe pas.")
            return redirect('ajoutEtudiantAdmin')

class DetailEtudiantAdmin(View):
    def get(self, request, uid):
        if request.user.is_authenticated:
            title = "Details Etudiant"
            now = datetime.today().strftime('%A %d %B %Y, %H:%M')
            try:
                item = Etudiant.objects.get(uid=uid)
                etudiants = Etudiant.objects.all()
                etudiant_count = Etudiant.objects.count()
            except Etudiant.DoesNotExist:
                messages.error(request, "Etudiant n'existe pas !")
                return redirect("ajoutEtudiantAdmin")
            return render(request, "app/admin/details_etudiant.html", {'title': title,'now': now,'item': item,'etudiants':etudiants, 'etudiant_count':etudiant_count })

class ChatEtudiant(View):
    def get(self, request):
        if request.user.is_authenticated:
            template_name = "app/etudiant/chat.html"
            title = "Ajout Etudiant"
            now = datetime.today().strftime('%A %d %B %Y, %H:%M')
            users = User.objects.filter(is_superuser=False).exclude(id=request.user.id)
            return render(request, template_name, {'title': title, 'now': now, 'users': users })

class DiscutionEtudiant(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            template_name = "app/etudiant/discussion.html"
            title = "Message"
            now = datetime.today().strftime('%A %d %B %Y, %H:%M')
            users = User.objects.filter(is_superuser=False).exclude(id=request.user.id)
            destinateur = get_object_or_404(User, id=id)
            messages = Message.objects.filter(expediteur=request.user, destinateur=destinateur) | Message.objects.filter(expediteur=destinateur, destinateur=request.user).order_by('date_envoi')
            return render(request, template_name, {'title': title, 'now': now, 'users': users, 'destinateur':destinateur, 'messages':messages,})

    def post(self, request, id):
        if request.user.is_authenticated:
            destinateur = get_object_or_404(User, id=id)
            message_contenu = request.POST['message']
            Message.objects.create(expediteur=request.user, destinateur=destinateur, contenu=message_contenu)
        return redirect("discutionEtudiant", id=id)

class DeleteMessage(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                item = Message.objects.get(id=id)
                if item.expediteur == request.user:
                    item.delete()
            except Message.DoesNotExist:
                messages.error(request, "Message n'a pas pu être supprimé. Il n'existe pas.")
            return redirect("discutionEtudiant", id=item.destinateur.id)

class Disconnect(View):
    def get(self, request):
        logout(request)
        return redirect('connect')