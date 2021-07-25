from django.urls import path

from CRM_TECH import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_ticket, name="new_ticket"),
    path(
        'tickets/<int:ticket_id>/',
        views.ticket_edit_staff,
        name='ticket_edit_staff',
    ),
    path(
        '<str:username>/<int:ticket_id>/',
        views.ticket_view,
        name='ticket_view'
    ),
    path(
        '<str:username>/<int:ticket_id>/edit/',
        views.ticket_edit,
        name='ticket_edit',
    ),
    path(
        'alltickets/',
        views.TiketsListView.as_view(),
        name='all_tickets',
    )
]
