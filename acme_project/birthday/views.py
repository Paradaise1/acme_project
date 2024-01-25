from django.core.paginator import Paginator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


ITEMS_PER_PAGE = 3 # Поменять на 10 когда БД будет больше


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = ITEMS_PER_PAGE


class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["birthday_countdown"] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context


# -------- Не используя CBV ------------
    
# from django.shortcuts import (
#     get_list_or_404,
#     get_object_or_404,
#     redirect,
#     render)


# def birthday(request, pk=None):
#     if pk is not None:
#         instance = get_object_or_404(Birthday, pk=pk)
#     else:
#         instance = None
#     form = BirthdayForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=instance
#     )
#     context = {'form': form}
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})

#     return render(request, 'birthday/birthday.html', context)


# def birthday_list(request):
#     birthdays = get_list_or_404(Birthday.objects.order_by('id'))

#     paginator = Paginator(birthdays, ITEMS_PER_PAGE)
#     page_namber = request.GET.get('page')
#     page_obj = paginator.get_page(page_namber)

#     context = {
#         'page_obj': page_obj,
#     }
#     return render(request, 'birthday/birthday_list.html', context)
    

# def delete_birthday(request, pk):
#     instance = get_object_or_404(Birthday, pk=pk)
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     if request.method == 'POST':
#         instance.delete()
#         return redirect('birthday:list')
#     return render(request, 'birthday/birthday.html', context)
