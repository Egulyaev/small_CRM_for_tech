from django.urls import path

from CRM_TECH import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_ticket, name="new_ticket"),
    path(
        '<str:username>/<int:ticket_id>/',
        views.ticket_view,
        name='ticket_view'
    ),
]