from django.forms import ModelForm
from webapp.models import Ticket, UserFollows


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'user']



class UserFollowForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
