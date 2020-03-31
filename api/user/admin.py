from django.contrib import admin
from user.models import (
    User,
    UserQuiz,
    UserAnswer,
)

admin.site.register(User)
admin.site.register(UserQuiz)
admin.site.register(UserAnswer)
