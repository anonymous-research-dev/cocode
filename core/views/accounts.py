from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic
from core.models import User
from core.forms import UserCreationForm, UserChangeForm


def user_signup_agreements(request):
    return render(
        request,
        'registration/signup_agreements.html',
    )
    
class UserCreateView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('login')

@method_decorator(login_required, name='dispatch')
class UserUpdateView(generic.UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'registration/edit_profile.html'

    def get_object(self):
        self.object = User.objects.get(id=self.request.user.id)
        return self.object

    def get_success_url(self):
        return reverse('manage')

