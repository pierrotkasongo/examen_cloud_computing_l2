from django.urls import path
from .views import *

urlpatterns = [
    path("", Connect.as_view(), name="connect"),
    path("dashboardAdmin", DashboardAdmin.as_view(), name="dashboardAdmin"),
    path("ajoutEtudiantAdmin", AjoutEtudiantAdmin.as_view(), name="ajoutEtudiantAdmin"),
    path("updateEtudiantAdmin/<str:uid>", UpdateEtudiantAdmin.as_view(), name="updateEtudiantAdmin"),
    path("deleteEtudiantAdmin/<str:uid>", DeleteEtudiantAdmin.as_view(), name="deleteEtudiantAdmin"),
    path("detailEtudiantAdmin/<str:uid>", DetailEtudiantAdmin.as_view(), name="detailEtudiantAdmin"),
    path("chatEtudiant", ChatEtudiant.as_view(), name="chatEtudiant"),
    path("discutionEtudiant/<int:id>", DiscutionEtudiant.as_view(), name="discutionEtudiant"),
    path("discutionEtudiant/<int:id>", DiscutionEtudiant.as_view(), name="discutionEtudiant"),
    path('deleteMessage/<int:id>/', DeleteMessage.as_view(), name='deleteMessage'),
    path("disconnect", Disconnect.as_view(), name="disconnect")
]