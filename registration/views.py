from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.views import generic

"""
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('/login')

    else:
        form = RegistrationForm(request.POST)

    return render(request, 'registration/register.html', {'form': form})

"""


class SignUpView(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"
