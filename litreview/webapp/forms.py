from django.forms import ModelForm
from webapp.models import Ticket


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'user']
