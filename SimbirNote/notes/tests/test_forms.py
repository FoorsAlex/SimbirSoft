import http
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from accounts.models import CustomUser
from ..models import Note


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class CreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_auth = CustomUser.objects.create(username='author@mail.ru')
        cls.authorized_user = Client()
        cls.guest_user = Client()
        cls.authorized_user.force_login(cls.user_auth)
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
            text='Тестовый текст',
            author=cls.user_auth,
            image=cls.uploaded
        )
        cls.reverse_login = reverse('account_login')
        cls.reverse_create = reverse('notes:note_create')

    def test_create_authorized_user(self):
        """Валидная форма создает запись в Note."""

        tasks_count = Note.objects.count()
        form_data = {
            'text': 'Тестовый текст1',
            'author': self.user_auth,
            'image': self.note.image
        }
        response = self.authorized_user.post(
            reverse('notes:note_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(Note.objects.count(), tasks_count + 1)
        self.assertTrue(
            Note.objects.filter(
                text=form_data['text'],
                author=form_data['author'],
            ).exists()
        )
        fields = {
            'text': Note.objects.get(author=self.user_auth, id=2).text,
            'author': self.note.author,
        }
        for field, expected_field in fields.items():
            with self.subTest(field=field):
                self.assertEqual(form_data[field], expected_field)
        self.assertIsInstance(self.note.image, ImageFieldFile)

    def test_edit(self):
        """Валидная форма редактирует запись в Note."""

        tasks_count = Note.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'author': self.user_auth,
            'image': self.uploaded.name
        }
        response = self.authorized_user.post(
            reverse('notes:note_edit', kwargs={'note_id': self.note.pk}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertRedirects(response, reverse(
            'notes:note_detail', kwargs={'note_id': self.note.id}))
        self.assertEqual(Note.objects.count(), tasks_count)
        self.assertTrue(
            Note.objects.filter(
                text=form_data['text'],
                author=form_data['author'],
                image=self.note.image
            ).exists()
        )
