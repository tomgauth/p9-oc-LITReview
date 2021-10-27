from django.forms import ModelForm, ChoiceField
from webapp.models import Ticket, UserFollows, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'user']



class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollows
        # field = ChoiceField(choices = ('a','b','c'))
        fields = ['followed_user']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
