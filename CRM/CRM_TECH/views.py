from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin

from .filters import TicketModelFilter
from .forms import TicketFormUser, TicketFormStaff, UserForm
from .models import Ticket, User
from .tables import TicketTable, UserTable

MAX_TICKET_PER_PAGE = 5


@login_required
def index(request):
    """Главная страница"""
    ticket_list = Ticket.objects.filter(author=request.user)
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
    form = TicketFormUser(request.POST or None)
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
    """Страница одного тикета"""
    author = get_object_or_404(User, username=username)
    ticket = get_object_or_404(Ticket, pk=ticket_id, author__username=username)
    return render(
        request,
        'tickets/ticket.html',
        {'ticket': ticket, 'author': author}
    )


@login_required
def ticket_edit(request, username, ticket_id):
    """Редактирование тикета"""
    ticket = get_object_or_404(Ticket, pk=ticket_id, author__username=username)
    if request.user != ticket.author:
        return redirect(
            ticket_view,
            username=username,
            ticket_id=ticket.pk,
        )
    form = TicketFormUser(
        request.POST or None,
        files=request.FILES or None,
        instance=ticket
    )
    if request.method == "GET" or not form.is_valid():
        return render(
            request,
            'tickets/new.html',
            {'form': form, 'is_edit': True}
        )
    ticket.save()
    return redirect(
        ticket_view,
        username=username,
        ticket_id=ticket.pk,
    )


@login_required
def ticket_edit_staff(request, ticket_id):
    """Редактирование всех полей тикета"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if not (
            request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
    ):
        return redirect(index)
    form = TicketFormStaff(
        request.POST or None,
        files=request.FILES or None,
        instance=ticket
    )
    if request.method == "GET" or not form.is_valid():
        return render(
            request,
            'tickets/edit_ticket_admin.html',
            {'form': form, 'is_edit': True}
        )
    ticket.save()
    return redirect(index)


@login_required
def user_edit(request, username):
    """Редактирование пользователя"""
    user = get_object_or_404(User, username=username)
    if (
            request.user.is_admin
            or request.user.is_superuser
            or request.user == user
    ):
        form = UserForm(
            request.POST or None,
            instance=user
        )
        if request.method == "GET" or not form.is_valid():
            return render(
                request,
                'tickets/new.html',
                {'form': form, 'is_edit': True}
            )
        user.save()
        return redirect(index)
    return redirect(index)


@method_decorator(login_required, name='dispatch')
class TiketsListView(SingleTableMixin, FilterView):
    model = Ticket
    table_class = TicketTable
    template_name = 'tickets/table.html'
    filterset_class = TicketModelFilter

    def dispatch(self, request, *args, **kwargs):
        if not (
                request.user.is_admin
                or request.user.is_superuser
                or request.user.is_moderator
        ):
            return redirect(index)
        return super(TiketsListView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UserListView(SingleTableView):
    model = User
    table_class = UserTable
    template_name = 'tickets/table.html'

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_admin or request.user.is_superuser):
            return redirect(index)
        return super(UserListView, self).dispatch(request, *args, **kwargs)
