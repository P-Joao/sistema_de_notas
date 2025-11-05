from django.db import models
from django.contrib.auth.models import User  # Importa o User embutido
from django.core.validators import MinValueValidator, MaxValueValidator  # Importa validadores já existentes do Django
# Create your models here.

class Professor(models.Model):
    # OneToOneField  "estende" o User. Cada User só pode ser
    # um Professor, e cada Professor é um User.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor")
    
    matricula = models.CharField(max_length=20, unique=True, null=False, blank=False, verbose_name="Matrícula")
    # Campos como nome e e-mail já estão no 'user' (user.first_name, user.email)
    
    def __str__(self):
        # Busca o nome completo (ou username) do User associado
        return self.user.get_full_name() or self.user.username
    
class Aluno(models.Model):
    # Mesmo padrão do Professor.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")

    matricula = models.CharField(max_length=20, unique=True, null=False, blank=False, verbose_name="Matrícula")
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
class Disciplina(models.Model):
    nome = models.CharField(max_length=200)

    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False, help_text="Código único da disciplina (Ex: COMP123)")

    def __str__(self):
        return self.nome
    
class Turma(models.Model):
    """
    Entidade associativa principal que "junta" as outras entidades.
    Representa uma oferta de uma Disciplina, com um Professor e Alunos.
    """
    
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False, help_text="Código único da turma (Ex: COMP123-2025.1-A)")

    # "Cada turma possui: uma disciplina" -> ForeignKey
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name="turmas")
    
    # "Cada turma possui: um professor" -> ForeignKey
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name="turmas")
    
    # "Cada turma possui: n alunos" -> ManyToManyField
    # Uma turma tem vários alunos; um aluno pode estar em várias turmas.
    alunos = models.ManyToManyField(Aluno, related_name="turmas")
    
    # Campos de contexto adicionais
    ano = models.IntegerField(default=2025)
    semestre = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])

    def __str__(self):
        return f"{self.disciplina.nome} ({self.ano}.{self.semestre}) - Prof. {self.professor}"
    
class Avaliacao(models.Model):
    """
    Define o "o quê" da avaliação (ex: Prova 1, Trabalho Final).
    Esse modelo é o TEMPLATE da avaliação.
    """
    
    # "n avaliações (que podem ser provas ou trabalhos com pesos diferentes)"
    # Cada avaliação pertence a UMA turma.
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="avaliacoes")
    
    titulo = models.CharField(max_length=100, blank=False, null=False, verbose_name="Título da Avaliação")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição da Avaliação")
    
    # "com pesos diferentes"
    peso = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0)], help_text="O peso desta avaliação na média final (ex: 4.0)")

    def __str__(self):
        return f"{self.titulo} (Peso {self.peso}) - {self.turma.disciplina.codigo}"

class Nota(models.Model):
    """
    Registro do *quanto* um aluno tirou em uma avaliação.
    """
    
    # ForeignKey de qual aluno se refere a nota.
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="notas")
    
    # ForeignKey de qual avaliação se refere a nota.
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name="notas")
    
    # O valor da nota.
    valor = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Nota")

    class Meta:
        # Garante que um aluno não tenha duas notas para a mesma avaliação
        unique_together = ('aluno', 'avaliacao')

    def __str__(self):
        return f"Nota {self.valor} para {self.aluno} em {self.avaliacao.titulo}"