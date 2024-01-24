from django.core.paginator import Paginator
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    redirect,
    render)

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


ITEMS_PER_PAGE = 3 # Поменять на 10 когда БД будет больше

def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})

    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    birthdays = get_list_or_404(Birthday.objects.order_by('id'))
    birthday_countdown_list = [
        calculate_birthday_countdown(item.birthday) for item in birthdays
    ]

    paginator = Paginator(birthdays, ITEMS_PER_PAGE)
    page_namber = request.GET.get('page')
    page_obj = paginator.get_page(page_namber)

    left = (int(page_namber) - 1) * ITEMS_PER_PAGE if page_namber else 0
    right = left + len(page_obj.object_list)

    context = {
        'page_obj': page_obj,
        'birthday_countdown_list': birthday_countdown_list[left:right]
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
