from django.contrib import admin
from user.models import (
    User,
    QuizUser,
    QuestionUser,
)

admin.site.register(User)
admin.site.register(QuizUser)
admin.site.register(QuestionUser)
