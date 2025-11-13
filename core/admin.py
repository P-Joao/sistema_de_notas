from django.contrib import admin
from .models import Professor, Aluno, Disciplina, Turma, Avaliacao, Nota  # Importando modelos

# Register your models here.

# -------------------------------------------------
# Personalização "In-line" para Matrículas
# Isso permite matricular alunos de dentro da tela da Turma
# -------------------------------------------------

# admin.TabularInline: Diz que queremos um formato de "tabela".
class AlunoInline(admin.TabularInline):
    model = Turma.alunos.through  # Pega a tabela de junção N:M
    verbose_name = "Aluno Matriculado"
    verbose_name_plural = "Alunos Matriculados"
    extra = 1  # Quantos campos em branco mostrar por padrão

# -------------------------------------------------
# Personalização dos Modelos Principais
# -------------------------------------------------

# A classe ProfessorAdmin "herda" de admin.ModelAdmin, que é o molde padrão do Django.
# Apenas "sobrescreve-se" as configurações que queremos mudar.
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    # Define quais colunas você vê na lista de todos os professores.
    list_display = ('__str__', 'matricula', 'user_email')

    # Adiciona uma barra de busca no topo da página.
    search_fields = ('user__first_name', 'user__last_name', 'matricula')
    
    # Helper para pegar o email do User
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'matricula', 'user_email')
    search_fields = ('user__first_name', 'user__last_name', 'matricula')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo')
    search_fields = ('nome', 'codigo')

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'professor', 'codigo', 'ano', 'semestre')
    search_fields = ('disciplina__nome', 'professor__user__first_name', 'codigo')

    # Adiciona uma barra lateral de filtros rápidos.
    list_filter = ('ano', 'semestre', 'disciplina')
    
    # Adiciona o "inline" de Alunos na página da Turma
    inlines = [AlunoInline]
    
    # Exclui o campo 'alunos' do formulário principal, já que estamos usando o inline
    exclude = ('alunos',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'turma', 'peso')
    search_fields = ('titulo', 'turma__disciplina__nome')
    list_filter = ('turma',)

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'avaliacao', 'valor')
    search_fields = ('aluno__user__first_name', 'avaliacao__titulo')
    list_filter = ('avaliacao__turma',)