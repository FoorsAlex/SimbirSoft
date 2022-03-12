import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Note
from accounts.models import CustomUser

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestPages(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_auth = CustomUser.objects.create(username='author@mail.ru')
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.note = Note.objects.create(
            text='Текст',
            author=cls.user_auth,
            image=cls.uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client_authorized = Client()
        self.client_authorized_user = Client()
        self.client_authorized.force_login(self.user_auth)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_pages_names = {
            'notes/save_notes.html': reverse('notes:save_notes'),
            'notes/index.html': reverse('notes:index'),
            'notes/note_detail.html': reverse(
                'notes:note_detail', kwargs={'note_id': self.note.pk}
            ),
            'notes/create_note.html': reverse(
                'notes:note_edit', kwargs={'note_id': self.note.pk}
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client_authorized.get(reverse_name)
                self.assertTemplateUsed(response, template)
        response = self.client_authorized.get(reverse('notes:note_create'))
        self.assertTemplateUsed(response, 'notes/create_note.html')

    def test_create_page_show_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""

        response = self.client_authorized.get(reverse('notes:note_create', ))
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_page_show_correct_context(self):
        """Шаблон note_edit сформирован с правильным контекстом."""

        response = self.client_authorized.get(
            reverse('notes:note_edit', kwargs={'note_id': self.note.pk}))
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_note_detail_pages_show_correct_context(self):
        """Шаблон note_detail сформирован с правильным контекстом."""

        response = (self.client_authorized.get(
            reverse('notes:note_detail', kwargs={'note_id': self.note.pk})
        )
        )
        self.assertEqual(response.context.get('note').text, self.note.text)
        self.assertEqual(response.context.get('note').author, self.user_auth)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(username='author@mail.ru')
        count_post_obj = 13
        object_post = [
            Note(
                text=f'Текст {i}',
                author=cls.user,
            )
            for i in range(0, count_post_obj)
        ]
        Note.objects.bulk_create(object_post)

    def setUp(self):
        self.client_authorized = Client()
        self.client_authorized.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """Проверка работы паджинатора 1-я страница"""

        count_pages = 10
        reverse_list = {
            'notes:save_notes': (),
        }
        for reverse_url, kwargs in reverse_list.items():
            with self.subTest(reverse_url=reverse_url):
                response = self.client_authorized.get(
                    reverse(reverse_url)
                )
                self.assertEqual(
                    len(response.context['page_obj']), count_pages, reverse_url)

    def test_second_page_contains_three_records(self):
        """Проверка работы паджинатора 2-я страница"""

        count_pages = 3
        reverse_list = {
            'notes:save_notes': (),
        }
        for reverse_url, kwargs in reverse_list.items():
            with self.subTest(reverse_url=reverse_url):
                response = self.client_authorized.get(
                    reverse(reverse_url) + '?page=2'
                )
                self.assertEqual(
                    len(response.context['page_obj']), count_pages
                )