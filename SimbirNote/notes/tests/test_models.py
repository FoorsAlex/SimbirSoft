from django.test import TestCase

from accounts.models import CustomUser
from ..models import Note


class NoteModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(username='auth@mail.ru')
        cls.note = Note.objects.create(
            author=cls.user,
            text='Тестовая группа'
        )

    def test_models_have_correct_object_names(self):
        """Проверка работы __str__"""

        note = NoteModelTest.note
        objects_names = {
            'note': [note, note.text[:15]],
        }
        for objects, name in objects_names.items():
            with self.subTest(objects=objects):
                self.assertEqual(str(name[0]), name[1])

    def test_labels_verbose_name(self):
        """verbose_name полей совпадает с ожидаемым."""

        note = NoteModelTest.note
        objects_labels = {
            'note_text': [note, 'text', 'Текст'],
        }
        for label, verbose_name in objects_labels.items():
            with self.subTest(label=label):
                verbose = verbose_name[0]._meta.get_field(
                    verbose_name[1]).verbose_name
                self.assertEqual(verbose, verbose_name[2])

    def test_labels_help_text(self):
        """help_text полей совпадает с ожидаемым."""

        note = NoteModelTest.note
        objects_labels = {
            'note_text': [note,
                          'text',
                          'Напишите о чём хотели-бы рассказать'
                          ],
        }
        for label, help_text in objects_labels.items():
            with self.subTest(label=label):
                verbose = help_text[0]._meta.get_field(help_text[1]).help_text
                self.assertEqual(verbose, help_text[2])
