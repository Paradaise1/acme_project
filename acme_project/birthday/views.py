from django.shortcuts import render

from .forms import BirthdayForm

from .utils import calculate_birthday_countdown


def birthday(request):
    form = BirthdayForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
        
    return render(request, 'birthday/birthday.html', context=context)
