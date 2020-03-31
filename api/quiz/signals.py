from django.db.models.signals import post_save
from django.dispatch import receiver
from quiz.models import Quiz
from quiz.tasks import resize_quiz_image, resize_quiz_photo_command


@receiver(post_save, sender=Quiz)
def resize_quiz_image_signal(sender, instance, created, **kwargs):
    print("Im inside post_save signal")
    resize_quiz_image.apply_async((instance.pk,))


# Other way ..
# post_save.connect(resize_quiz_image, sender=Quiz)
