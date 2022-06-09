from django.shortcuts import render, redirect
from .forms import RegistrationForm


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('/poll')

    else:
        form = RegistrationForm(request.POST)

    return render(request, 'registration/register.html', {'form': form})
