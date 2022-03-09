from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('text', 'image')
        labels = {
            'text': 'Текст',
        }
        help_texts = {
            'text': 'Содержание записи',
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Воу! Это обязательное поле')
        return data


