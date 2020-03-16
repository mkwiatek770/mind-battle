from django.contrib import admin
from user.models import (
    QuizUser,
    QuestionUser,
)


admin.site.register(QuizUser)
admin.site.register(QuestionUser)
