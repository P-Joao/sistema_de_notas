from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import Avaliacao, Nota, Aluno, Turma
from .forms import AvaliacaoForm
from django.http import HttpResponse


@login_required # Garante que apenas usuários logados acessem
def lancar_notas(request, avaliacao_id):
    
    # 1. Pega os objetos principais do banco
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    turma = avaliacao.turma
    
    # 2. AUTORIZAÇÃO: Checa se o usuário é o professor da turma
    try:
        # Tenta acessar o perfil de professor do usuário logado
        if turma.professor != request.user.professor:
            # Se não for, nega o acesso e carrega o template de erro
            return render(request, 'core/acesso_negado.html')
    except AttributeError:
        # Se der erro (ex: é um Aluno logado), nega o acesso
        # (A menos que seja um Admin/Staff)
        if not request.user.is_staff:
            return render(request, 'core/acesso_negado.html')

    # 3. CRIA A "FÁBRICA DE FORMULÁRIOS"
    # Queremos um formset que edite APENAS o campo 'valor' do modelo Nota
    # 'extra=0' impede que ele crie campos para notas novas
    NotaFormSet = modelformset_factory(Nota, fields=('valor',), extra=0)

    # 4. PRÉ-POPULAÇÃO (A MÁGICA)
    # Garante que CADA aluno da turma tenha um objeto 'Nota'
    # para esta avaliação, mesmo que seja uma nota 0.
    
    alunos_da_turma = turma.alunos.all()
    # IDs dos alunos que JÁ têm um registro de nota
    alunos_com_nota = Nota.objects.filter(avaliacao=avaliacao).values_list('aluno_id', flat=True)
    
    for aluno in alunos_da_turma:
        if aluno.id not in alunos_com_nota:
            # Cria a nota "em branco" (com 0) para o aluno que não tem
            Nota.objects.create(aluno=aluno, avaliacao=avaliacao, valor=0.0)
            
    # 5. DEFINE O QUERYSET
    # Agora que todos os registros de nota existem, dizemos ao formset
    # para gerenciar apenas as notas desta avaliação e desta turma.
    # O .select_related() otimiza a busca no banco
    queryset = Nota.objects.filter(
        avaliacao=avaliacao, 
        aluno__in=alunos_da_turma
    ).select_related('aluno__user') # Puxa Aluno e User numa só query

    # 6. PROCESSA O POST (QUANDO O PROFESSOR SALVA)
    if request.method == 'POST':
        formset = NotaFormSet(request.POST, queryset=queryset)
        
        if formset.is_valid():
            formset.save() # Salva TODAS as notas de uma vez
            # Redireciona para a mesma página
            return redirect('lancar_notas', avaliacao_id=avaliacao.id)
    
    # 7. PROCESSA O GET (QUANDO O PROFESSOR ABRE A PÁGINA)
    else:
        formset = NotaFormSet(queryset=queryset)

    # 8. ENVIA OS DADOS PARA O TEMPLATE
    context = {
        'formset': formset,
        'avaliacao': avaliacao,
    }
    return render(request, 'core/lancar_notas.html', context)

@login_required
def criar_avaliacao(request, turma_id):
    
    # 1. Pega a turma
    turma = get_object_or_404(Turma, id=turma_id)
    
    # 2. AUTORIZAÇÃO: Checa se o usuário é o professor da turma
    try:
        if turma.professor != request.user.professor:
            return render(request, 'core/acesso_negado.html')
    except AttributeError:
        if not request.user.is_staff:
            return render(request, 'core/acesso_negado.html')

    # 3. PROCESSA O POST (QUANDO O PROFESSOR SALVA)
    if request.method == 'POST':
        # Cria uma instância do formulário com os dados enviados
        form = AvaliacaoForm(request.POST)
        
        if form.is_valid():
            # 'commit=False' cria o objeto em memória, mas não salva no banco
            avaliacao = form.save(commit=False)
            
            # 4. LIGA A AVALIAÇÃO À TURMA (da URL)
            avaliacao.turma = turma
            
            # Salva no banco
            avaliacao.save()
            
            # 5. REDIRECIONA para a página de lançar notas DESSA avaliação
            return redirect('lancar_notas', avaliacao_id=avaliacao.id)
    
    # 6. PROCESSA O GET (QUANDO O PROFESSOR ABRE A PÁGINA)
    else:
        # Cria um formulário em branco
        form = AvaliacaoForm()

    # 7. ENVIA OS DADOS PARA O TEMPLATE
    context = {
        'form': form,
        'turma': turma,
    }
    return render(request, 'core/criar_avaliacao.html', context)

@login_required
def home(request):
    # 1. Painel do PROFESSOR
    if hasattr(request.user, 'professor'):
        # Busca as turmas desse professor
        turmas = request.user.professor.turmas.all().select_related('disciplina')
        context = {'turmas': turmas}
        return render(request, 'core/dashboard_professor.html', context)

    # 2. Painel do ALUNO
    elif hasattr(request.user, 'aluno'):
        # Busca as notas desse aluno
        aluno_logado = request.user.aluno
        notas = Nota.objects.filter(aluno=aluno_logado).select_related(
            'avaliacao__turma__disciplina'
        )
        context = {'notas': notas}
        return render(request, 'core/dashboard_aluno.html', context)

    # 3. Superusuário
    elif request.user.is_superuser:
        return redirect('admin:index')

    else:
        return HttpResponse("Perfil não configurado.")
    
@login_required
def turma_detalhe(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Segurança: Garante que apenas o professor dono da turma acessa
    if hasattr(request.user, 'professor'):
         if turma.professor != request.user.professor:
             return render(request, 'core/acesso_negado.html')
    
    # Busca dados para exibir na tela
    avaliacoes = turma.avaliacoes.all()
    alunos = turma.alunos.all()

    context = {
        'turma': turma,
        'avaliacoes': avaliacoes,
        'alunos': alunos
    }
    return render(request, 'core/turma_detalhe.html', context)