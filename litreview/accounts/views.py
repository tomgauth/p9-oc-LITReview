from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # reverse_lazy redirects the user after creation
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
