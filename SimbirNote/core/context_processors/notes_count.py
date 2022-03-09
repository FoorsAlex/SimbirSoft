from notes.models import Note


def notes_count(request):
    user = request.user
    count = len(Note.objects.filter(author=user))
    return {
        'notes_count': count
    }
