from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # reverse_lazy redirects the user after creation
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


def home(request):
    return redirect('home')
