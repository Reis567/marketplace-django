# Importe os módulos e modelos necessários
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from django.contrib.auth.decorators import login_required
from .models import Conversation
from .forms import ConversationMessageForm

# Função de visualização para iniciar uma nova conversa
@login_required
def new_conversation(request, item_pk):
    # Obtenha o objeto do item com a chave primária (item_pk) fornecida do banco de dados
    item = get_object_or_404(Item, pk=item_pk)

    # Verifique se o usuário atual é o criador do item, se sim, redirecione para o painel (dashboard)
    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Consulte as conversas relacionadas ao item onde o usuário atual é um membro
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # Se já existirem conversas para este item e usuário, não faça nada (declaração "pass")
    if conversations:
        return redirect('conversation:detail',pk=conversations.first().id)

    # Trate o envio do formulário (se o método da requisição for POST)
    if request.method == 'POST':
        # Crie uma instância de ConversationMessageForm e popule com os dados da requisição
        form = ConversationMessageForm(request.POST)

        # Verifique se os dados do formulário são válidos
        if form.is_valid():
            # Crie um novo objeto Conversation e associe-o ao item atual
            conversation = Conversation.objects.create(item=item)
            # Adicione o usuário atual e o criador do item aos membros da conversa
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            # Salve o objeto conversation com os membros atualizados
            conversation.save()

            # Crie um novo objeto ConversationMessage, mas não o salve no banco de dados ainda
            conversation_message = form.save(commit=False)
            # Associe o conversation_message à nova conversa criada
            conversation_message.conversation = conversation
            # Defina o criador da mensagem como o usuário atual
            conversation_message.created_by = request.user
            # Salve o conversation_message no banco de dados
            conversation_message.save()

            # Redirecione o usuário para a página de detalhes do item após a criação bem-sucedida da conversa
            return redirect('item:detail', pk=item_pk)
        
    else:
        # Se o método da requisição não for POST, crie uma instância vazia do formulário
        form = ConversationMessageForm()

    # Renderize o template 'new.html' com os dados do formulário
    return render(request, 'conversation/new.html', {'form': form})


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html',{
        'conversations':conversations,
    })

@login_required
def detail(request,pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method=='POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail',pk=pk)
        

    else:
        form = ConversationMessageForm()

    return render(request,'conversation/detail.html',{
        'conversation':conversation,
        'form':form,
    })