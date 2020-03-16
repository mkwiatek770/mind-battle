from django.contrib import admin
from quiz.models import (
    Quiz,
    Question,
    Category,
    QuestionAnswer
)


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(Category)
