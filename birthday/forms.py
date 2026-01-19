from django import forms
from .models import Birthday
from .validators import real_age
from django.core.exceptions import ValidationError

BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(
        label='Фамилия', required=False, help_text='Необязательное поле'
    )
    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=(real_age,),
    )

    class Meta:
        model = Birthday
        fields = ['first_name', 'last_name', 'birthday']

    def __init__(self, *args, **kwargs):
        # Извлекаем instance из kwargs, если он передан
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # Если instance есть, заполняем поля значениями из модели
        if self.instance:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['birthday'].initial = self.instance.birthday

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return first_name

    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )
