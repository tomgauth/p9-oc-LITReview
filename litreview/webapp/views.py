from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Ticket, UserFollows, Review
from webapp.forms import TicketForm, UserFollowForm, ReviewForm
from django.contrib.auth.models import User
from django.db.models import Value, CharField
from django.db import IntegrityError
from itertools import chain

# Create your views here.


def feed(request):

    def get_followed_users_ids(user):
        followed_users = UserFollows.objects.filter(user=user)
        followed_users_ids = [pair.followed_user.id for pair in followed_users]
        return followed_users_ids

    def get_users_viewable_reviews(user, followed_users_ids):
        user_reviews = Review.objects.all().filter(user_id=user.id)
        followed_reviews = Review.objects.all().filter(user_id__in=followed_users_ids)
        reviews = list(chain(user_reviews, followed_reviews))
        for review in reviews:
            review.type = 'REVIEW'
        return reviews

    def get_user_reviewed_tickets(user, user_reviews):
        user_reviewed_tickets = []
        for user_review in user_reviews:
            user_reviewed_tickets.append(user_review.ticket)
        return user_reviewed_tickets

    def get_users_viewable_tickets(user, followed_users_ids):
        user_reviews = Review.objects.all().filter(user_id=user.id)
        user_tickets = Ticket.objects.all().filter(user_id=user.id)
        followed_tickets = Ticket.objects.all().filter(user_id__in=followed_users_ids)
        tickets = list(chain(user_tickets, followed_tickets))

        for ticket in tickets:
            ticket.type = 'TICKET'
            ticket.display = 'NORMAL'
            # if the user is one of the users in ticket.reviews
        return tickets


    user = request.user
    followed_users_ids = get_followed_users_ids(user)
    reviews = get_users_viewable_reviews(user, followed_users_ids)
    tickets = get_users_viewable_tickets(user, followed_users_ids)
    tickets_reviewed_by_user = list(Ticket.objects.filter(review__ticket__user=1))
    tickets_and_reviews = tickets + reviews

    posts = sorted(
        tickets + reviews,
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'feed.html', {'posts': posts,
                                         'tickets': tickets,
                                         'reviews': reviews,
                                         'tickets_reviewed_by_user': tickets_reviewed_by_user})

    # return render(request, 'feed.html', context={'posts': posts})


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


def followers(request):
    user = request.user
    subscribers = UserFollows.objects.filter(followed_user=user.id)
    subscriptions = UserFollows.objects.filter(user=user.id)
    user_follow_instance = UserFollows()
    found_user = ""
    if request.method == "GET":
        form = UserFollowForm()
        # get the ids of users already followed
        already_followed = [
            pair.followed_user.id for pair in UserFollows.objects.filter(user=user)]
        # remove the already followed users and the current user from the options
        options = User.objects.all().exclude(id__in=already_followed).exclude(id=user.id)
        result_list = list(chain(options, already_followed))
        form.fields['followed_user'].queryset = options
        return render(request, 'my_followers.html', locals())
    elif request.method == "POST":
        already_followed = [
            pair.followed_user.id for pair in UserFollows.objects.filter(user=user)]
        searched = request.POST['searched']
        # users = options.get(username__contains=searched)
        try:
            found_user = User.objects.get(username=searched.capitalize())
            user_follow_instance.user = user
            user_follow_instance.followed_user = found_user
            if user != found_user:
                user_follow_instance.save()
            else:
                error_message = "You cannot follow yourself!"
        except User.DoesNotExist:
            found_user = None
        except IntegrityError:
            found_user = None
            error_message = "You're already following this user"
        return render(request, 'my_followers.html', locals())


def delete_user_follow(request, user_follow_id):
    user_follows = get_object_or_404(UserFollows, pk=user_follow_id)
    user_follows.delete()
    return redirect('my_followers')


def my_reviews(request):
    user = request.user
    reviews = Review.objects.all().filter(user_id=user.id)
    return render(request, 'my_reviews.html', {'reviews': reviews})


def write_review_ticket(request, ticket_id):
    review_instance = Review()
    user = request.user
    ticket_instance = Ticket.objects.get(
        pk=ticket_id)
    review_instance.ticket = ticket_instance
    review_instance.user = user
    form = ReviewForm(instance=review_instance)
    if request.method == "GET":
        return render(request, 'write_review_ticket.html', locals())
    elif request.method == "POST":
        form = ReviewForm(request.POST, instance=review_instance)
        if form.is_valid():
            form.save()
            return redirect('my_reviews')


def edit_review(request, review_id):
    review_instance = Review.objects.get(pk=review_id)
    if request.method == "GET":
        form = ReviewForm(instance=review_instance)
        return render(request, 'edit_review.html', locals())
    elif request.method == "POST":
        form = ReviewForm(request.POST,
                      instance=review_instance)
    if form.is_valid():
        form.save()
        return redirect('my_reviews')



def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('my_reviews')







