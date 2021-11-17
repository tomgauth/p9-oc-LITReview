from django.forms import ModelForm, ChoiceField, RadioSelect, Form
from webapp.models import Ticket, UserFollows, Review
from bootstrap5.widgets import RadioSelectButtonGroup


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']



class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        widgets = {
          'rating': RadioSelect(),
        }
        choices=[1,2,3]
