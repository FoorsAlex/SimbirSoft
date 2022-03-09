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
def post_detail(request, post_id):
    post = get_object_or_404(Note, id=post_id)
    post_list = Note.objects.filter(author__username=post.author)
    count_posts = post_list.count()
    context = {
        'post': post,
        'count_posts': count_posts,
    }
    return render(request, 'notes/note_detail.html', context)


@login_required
def post_create(request):
    template = 'notes/create_note.html'
    client = request.user
    form = NoteForm(
        request.POST or None,
        files=request.FILES or None, )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = client
        post.save()
        return redirect('notes:save_notes')
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    template = 'notes/create_note.html'
    client = request.user
    post = get_object_or_404(Note, id=post_id)
    if post.author != client:
        return redirect('notes:post_detail', post_id=post_id)
    form = NoteForm(
        request.POST or None,
        instance=post,
        files=request.FILES or None
    )
    if form.is_valid():
        post.save()
        return redirect('notes:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': True,
        'template': template
    }
    return render(request, template, context)
