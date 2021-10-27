from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Ticket, UserFollows, Review
from webapp.forms import TicketForm, UserFollowForm, ReviewForm
from django.contrib.auth.models import User
from itertools import chain

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


def followers(request):
    user = request.user
    subscribers = UserFollows.objects.filter(followed_user=user.id)
    subscriptions = UserFollows.objects.filter(user=user.id)
    user_follow_instance = UserFollows()
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
        user_follow_instance.user = user
        form = UserFollowForm(request.POST, instance=user_follow_instance)
        if form.is_valid():
            form.save()
            return redirect('my_followers')


def create_user_follow(request):
    user_follow_instance = UserFollows()
    if request.method == "GET":
        user = request.user
        form = UserFollowForm()
        # get the ids of users already followed
        already_followed = [
            pair.followed_user.id for pair in UserFollows.objects.filter(user=user)]
        # remove the already followed users and the current user from the options
        options = User.objects.all().exclude(id__in=already_followed).exclude(id=user.id)
        result_list = list(chain(options, already_followed))
        form.fields['followed_user'].queryset = options
        return render(request, 'create_user_follow.html', locals())
    elif request.method == "POST":
        user_follow_instance.user = user
        form = UserFollowForm(request.POST, instance=user_follow_instance)
        if form.is_valid():
            form.save()
            return redirect('my_followers')


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







