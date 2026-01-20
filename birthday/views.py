from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from django.urls import reverse

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect


class BirthdayListView(ListView):
    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tags'
    ).select_related('author')
    ordering = 'id'
    paginate_by = 10


# Наследуем BirthdayCreateView от CreateView и от миксина LoginRequiredMixin:
class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)

    def birthday(request):
        form = BirthdayForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()


class BirthdayUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm

    def test_func(self):
        # Получаем текущий объект.
        object = self.get_object()
        # Метод вернёт True или False.
        # Если пользователь - автор объекта, то тест будет пройден.
        # Если нет, то будет вызвана ошибка 403.
        return object.author == self.request.user


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(LoginRequiredMixin, DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})


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
