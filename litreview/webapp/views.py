from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Ticket
from webapp.forms import TicketForm
# from itertools import chain

# Create your views here.


def feed(request):
    posts = [{'title': 'first post',
              'content': 'hello world'},
             {'title': 'need a review',
              'content': 'how good is this book?'}
             ]
#     reviews = get_users_viewable_reviews(request.user)
#     # returns queryset of reviews
#     reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

#     tickets = get_users_viewable_tickets(request.user)
#     # returns queryset of tickets
#     tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

#     # combine and sort the two types of posts
#     posts = sorted(
#         chain(reviews, tickets),
#         key=lambda post: post.time_created,
#         reverse=True
#     )
    return render(request, 'feed.html', context={'posts': posts})


def list_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'list_tickets.html', {'tickets': tickets})


def create_ticket(request, ticket_id=None):
    ticket_instance = Ticket.objects.get(
        pk=ticket_id) if ticket_id is not None else None
    if request.method == "GET":
        form = TicketForm(instance=ticket_instance)
        return render(request, 'create_ticket.html', locals())
    elif request.method == "POST":
        form = TicketForm(request.POST, request.FILES,
                          instance=ticket_instance)
        if form.is_valid():
            ticket = form.save()
            return redirect('list_tickets')


def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'view_ticket.html', locals())


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('list_tickets')
