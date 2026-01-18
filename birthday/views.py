from django.shortcuts import get_object_or_404, render, redirect
from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown
from django.core.paginator import Paginator
from django.urls import reverse


def birthday_list(request):
    # Получаем список всех объектов с сортировкой по id
    birthdays = Birthday.objects.order_by('id')
    paginator = Paginator(birthdays, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'birthdays': page_obj.object_list
    }
    return render(request, 'birthday/birthday_list.html', context)


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
