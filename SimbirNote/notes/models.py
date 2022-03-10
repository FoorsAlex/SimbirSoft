from accounts.models import CustomUser
from django.db import models


class Note(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Напишите о чём хотели-бы рассказать'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notes',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='notes/',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return self.text[:15]
