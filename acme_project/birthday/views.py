from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.urls import reverse, reverse_lazy

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown


ITEMS_PER_PAGE = 3 # Поменять на 10 когда БД будет больше


class BirthdayListView(ListView):
    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tags'
    ).select_related('author')
    ordering = 'id'
    paginate_by = ITEMS_PER_PAGE


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            self.object.congratulations.select_related('author')
        )
        return context
    

class CongratulationCreateView(LoginRequiredMixin ,CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})


# -------- Не используя CBV ------------

# from django.core.paginator import Paginator
# from django.shortcuts import (
#     get_list_or_404,
#     get_object_or_404,
#     redirect,
#     render)


# @login_required
# def birthday(request, pk=None):
#     if pk is not None:
#         instance = get_object_or_404(Birthday, pk=pk, author=request.user)
#     else:
#         instance = None
#     form = BirthdayForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=instance
#     )
#     context = {'form': form}
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.author = request.user
#         instance.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({
#             'birthday_countdown': birthday_countdown,
#             'form': CongratulationForm(),
#             'congratulations': (
#                 self.object.congratulations.select_related('author')
#             )
#         })

#     return render(request, 'birthday/birthday.html', context)


# @login_required
# def birthday_list(request):
#     birthdays = get_list_or_404(Birthday.objects.order_by('id'))

#     paginator = Paginator(birthdays, ITEMS_PER_PAGE)
#     page_namber = request.GET.get('page')
#     page_obj = paginator.get_page(page_namber)

#     context = {
#         'page_obj': page_obj,
#     }
#     return render(request, 'birthday/birthday_list.html', context)
    

# @login_required
# def delete_birthday(request, pk):
#     instance = get_object_or_404(Birthday, pk=pk)
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     if request.method == 'POST':
#         instance.delete()
#         return redirect('birthday:list')
#     return render(request, 'birthday/birthday.html', context)
    

# @login_required
# def add_comment(request, pk):
#     birthday = get_object_or_404(Birthday, pk=pk)
#     form = CongratulationForm(request.POST)
#     if form.is_valid():
#         congratulation = form.save(commit=False)
#         congratulation.author = request.user
#         congratulation.birthday = birthday
#         congratulation.save()
#     return redirect('birthday:detail', pk=pk)
