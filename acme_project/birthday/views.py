from django.shortcuts import render
from .forms import BirthdayForm


def birthday(request):
    form = BirthdayForm()
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context=context)
