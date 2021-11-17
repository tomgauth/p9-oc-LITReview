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

    def get_tickets_reviewed_by_user(user_reviews):
        tickets_reviewed_by_user = []
        for user_review in user_reviews:
            if user_review.ticket:
                tickets_reviewed_by_user.append(user_review.ticket)
        return tickets_reviewed_by_user

    user = request.user
    followed_users_ids = get_followed_users_ids(user)
    reviews = get_users_viewable_reviews(user, followed_users_ids)
    tickets = get_users_viewable_tickets(user, followed_users_ids)
    user_reviews = Review.objects.all().filter(user_id=user.id)
    tickets_reviewed_by_user = get_tickets_reviewed_by_user(user_reviews)


    tickets_and_reviews = tickets + reviews

    posts = sorted(
        tickets + reviews,
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'feed.html', {'nbar': 'feed',
                                         'posts': posts,
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
            obj = form.save(commit = False)
            obj.user_id = request.user.id
            obj.save()
            return redirect('posts')


def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'view_ticket.html', locals())


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('posts')


def followers(request):
    nbar = 'my_followers'
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
            found_user = User.objects.get(username__iexact=searched)
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


def write_review_and_ticket(request, ticket_id=None, review_id=None):
    ticket_instance = Ticket.objects.get(
        pk=ticket_id) if ticket_id is not None else None
    review_instance = Review.objects.get(
        pk=review_id) if review_id is not None else None
    if request.method == "GET":
        ticket_form = TicketForm(instance=ticket_instance)
        review_form = ReviewForm(instance=review_instance)
        return render(request, 'write_review_and_ticket.html', locals())
    elif request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES,
                          instance=ticket_instance)
        review_form = ReviewForm(request.POST, request.FILES,
                          instance=review_instance)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket_obj = ticket_form.save(commit = False)
            ticket_obj.user_id = request.user.id
            ticket_obj.save()
            review_obj = review_form.save(commit = False)
            review_obj.user_id = request.user.id
            review_obj.ticket = ticket_obj
            review_obj.save()
            return redirect('posts')


def write_review_ticket(request, ticket_id):
    ticket_instance = Ticket.objects.get(
        pk=ticket_id)
    if request.method == "GET":
        form = ReviewForm()
        return render(request, 'write_review_ticket.html', locals())
    elif request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_obj = form.save(commit = False)
            review_obj.user_id = request.user.id
            review_obj.ticket = ticket_instance
            review_obj.save()
            return redirect('posts')



def edit_review(request, review_id):
    review_instance = Review.objects.get(pk=review_id)
    rating = review_instance.rating
    if request.method == "GET":
        form = ReviewForm(instance=review_instance)
        return render(request, 'edit_review.html', locals())
    elif request.method == "POST":
        form = ReviewForm(request.POST,
                      instance=review_instance)
    if form.is_valid():
        form.save()
        return redirect('posts')



def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('posts')



def posts(request):
    # get all user's reviews
    user = request.user
    user_reviews = Review.objects.all().filter(user_id=user.id)
    for review in list(user_reviews):
        review.type = 'REVIEW'

    user_tickets = Ticket.objects.all().filter(user_id=user.id)
    for ticket in list(user_tickets):
        ticket.type = 'TICKET'

    # get all user's tickets
    tickets_reviewed_by_user = list(Ticket.objects.filter(review__ticket__user=user.id))
    posts = sorted(
        list(user_tickets) + list(user_reviews),
        # tickets + reviews,
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'posts.html', locals())



