"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp import views

urlpatterns = [
    path('feed', views.feed, name="feed"),

    path('tickets', views.list_tickets, name="list_tickets"),
    path('ticket/<int:ticket_id>', views.view_ticket, name="view_ticket"),
    path('create_ticket', views.create_ticket, name="create_ticket"),
    path('create_ticket/<int:ticket_id>', views.create_ticket, name="create_ticket"),
    path('delete_ticket/<int:ticket_id>', views.delete_ticket, name="delete_ticket"),

    path('my_followers', views.followers, name='my_followers'),
    path('delete_user_follow/<int:user_follow_id>', views.delete_user_follow, name="delete_user_follow"),

    path('my_reviews', views.my_reviews, name='my_reviews'),
    path('edit_review/<int:review_id>', views.edit_review, name="edit_review"),
    path('delete_review/<int:review_id>', views.delete_review, name="delete_review"),

    path('write_review_ticket', views.write_review_ticket, name='write_review_ticket'),
    path('write_review_ticket/<int:ticket_id>', views.write_review_ticket, name='write_review_ticket'),
    path('write_review_and_ticket', views.write_review_and_ticket, name='write_review_and_ticket'),

]
