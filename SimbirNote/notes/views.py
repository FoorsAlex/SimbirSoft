from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note


def index(request):
    template = 'notes/index.html'
    return render(request, template)


def get_paginator_obj(request, query_list):
    paginator = Paginator(query_list, settings.COUNT_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
def save_notes(request):
    templates = 'notes/save_notes.html'
    user = request.user
    post_list = Note.objects.filter(author=user)
    page_obj = get_paginator_obj(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, templates, context)


@login_required()
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    context = {
        'note': note,
    }
    return render(request, 'notes/note_detail.html', context)


@login_required
def note_create(request):
    template = 'notes/create_note.html'
    client = request.user
    form = NoteForm(
        request.POST or None,
        files=request.FILES or None, )
    if form.is_valid():
        note = form.save(commit=False)
        note.author = client
        note.save()
        return redirect('notes:save_notes')
    return render(request, template, {'form': form})


@login_required
def note_edit(request, note_id):
    template = 'notes/create_note.html'
    client = request.user
    note = get_object_or_404(Note, id=note_id)
    if note.author != client:
        return redirect('notes:note_detail', note_id=note_id)
    form = NoteForm(
        request.POST or None,
        instance=note,
        files=request.FILES or None
    )
    if form.is_valid():
        note.save()
        return redirect('notes:note_detail', note_id=note_id)
    context = {
        'form': form,
        'is_edit': True,
        'template': template
    }
    return render(request, template, context)


@login_required
def note_delete(request, note_id):
    user = request.user
    note = get_object_or_404(Note, id=note_id)
    if note.author == user:
        note.delete()
        return redirect('notes:save_notes')
    return redirect('account_login')
