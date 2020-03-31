import os
import io
from PIL import Image
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from quiz.models import Quiz


@shared_task
def resize_quiz_image(quiz_id: int) -> None:
    resize_quiz_photo_command(Quiz.objects.get(id=quiz_id))


def resize_quiz_photo_command(quiz: int) -> None:
    """Resize image of single quiz object."""
    if quiz.image.name == 'default_quiz.jpeg':
        return

    memfile = io.BytesIO()
    img = Image.open(quiz.image)

    output_size = (400, 300)
    img.thumbnail(output_size, Image.ANTIALIAS)
    img.save(memfile, 'JPEG', quality=95)

    old_image = quiz.image
    old_image_name = old_image.name

    default_storage.delete(old_image.name)
    quiz.image.save(old_image_name, ContentFile(memfile.getvalue()))
