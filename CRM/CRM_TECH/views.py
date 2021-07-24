from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TicketForm
from .models import Ticket, User

MAX_TICKET_PER_PAGE = 5

def index(request):
    """Главная страница"""
    ticket_list = Ticket.objects.all()
    paginator = Paginator(ticket_list, MAX_TICKET_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'tickets/index.html',
        {'page': page}
    )

@login_required
def new_ticket(request):
    """Страница создания нового тикета"""
    form = TicketForm(request.POST or None)
    if request.method == "GET" or not form.is_valid():
        return render(
            request,
            "tickets/new.html",
            {"form": form, "is_edit": False}
        )
    ticket = form.save(commit=False)
    ticket.author = request.user
    ticket.save()

    return redirect("index")

@login_required
def ticket_view(request, username, ticket_id):
    """Страница тикета с комментариями"""
    author = get_object_or_404(User, username=username)
    ticket = get_object_or_404(Ticket, pk=ticket_id, author__username=username)

    return render(
        request,
        'tickets/ticket.html',
        {'ticket': ticket, 'author': author}
    )