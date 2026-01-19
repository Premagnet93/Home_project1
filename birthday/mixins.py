from django.contrib import messages


class BirthdayMixin:
    """Базовый миксин для работы с днями рождения."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте нужные данные в контекст
        context['is_birthday_page'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Данные успешно сохранены!')
        return super().form_valid(form)
