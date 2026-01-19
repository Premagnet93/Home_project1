# birthday/views.py
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown

class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10

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
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context


"""
from django.shortcuts import get_object_or_404, render, redirect
from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from .mixins import BirthdayMixin


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)

    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')

    context = {
        'form': BirthdayForm(instance=instance),
        'instance': instance
    }
    return render(request, 'birthday/birthday.html', context)


def birthday_detail(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(
        request.POST or None,
        instance=instance
    )

    if form.is_valid():
        form.save()
        return redirect('birthday:list')

    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'birthday/birthday.html', context)


class BirthdayCreateView(BirthdayMixin, CreateView):
    model = Birthday
    # Указываем имя формы:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
"""