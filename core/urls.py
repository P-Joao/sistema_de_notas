from django.urls import path
from . import views  # Importa as views do app 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('avaliacao/<int:avaliacao_id>/notas/', views.lancar_notas, name='lancar_notas'),
    path('turma/<int:turma_id>/criar-avaliacao/', views.criar_avaliacao, name='criar_avaliacao'),
]