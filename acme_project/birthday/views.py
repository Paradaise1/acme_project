from django.shortcuts import get_list_or_404, render

from .forms import BirthdayForm

from .models import Birthday

from .utils import calculate_birthday_countdown


def birthday(request):
    form = BirthdayForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
        
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    birthdays = get_list_or_404(Birthday)
    #sorted(birthdays, key=lambda x: x.id)
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context)
