from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    redirect,
    render)

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(request.POST or None, instance=instance)
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
    birthday_countdown_list = [
        calculate_birthday_countdown(item.birthday) for item in birthdays
    ]
    context = {
        'birthdays': birthdays,
        'birthday_countdown_list': birthday_countdown_list
    }
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    return render(request, 'birthday/birthday.html', context)
