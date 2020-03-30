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


def resize_quiz_photo_command(quiz: Quiz):
    _, extension = os.path.splitext((quiz.image.url.split("?")[0]))
    photo = default_storage.open(quiz.image.url)
    resized_photo = Image.open(photo.file).resize((300, 200), Image.ANTIALIAS)
    b = io.BytesIO()
    resized_photo.save(b, format=extension[1:])
    resp = default_storage.save(quiz.image.url, ContentFile(b.getvalue()))
#    quiz.cover_photo = os.path.join('books', os.path.basename(resp))
    quiz.save()


def resize_quiz_photo_command_v2(quiz: int) -> None:
    memfile = io.BytesIO()

    img = Image.open(quiz.image)

    output_size = (400, 300)
    img.thumbnail(output_size, Image.ANTIALIAS)
    img.save(memfile, 'JPEG', quality=95)
    # default_storage.save(quiz.image.name, memfile)
    memfile.close()
    img.close()

    # quiz.image.save(img)
    # import pdb
    # pdb.set_trace()
    # quiz.image = img
    # quiz.save()
