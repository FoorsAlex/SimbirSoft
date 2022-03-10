from notes.models import Note


def notes_count(request):
    if request.user.is_authenticated:
        user = request.user
        count = len(Note.objects.filter(author=user))
    else:
        count = None
    return {
        'notes_count': count
    }
