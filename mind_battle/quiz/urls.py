from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from quiz import views
from quiz.router import NestedDefaultRouter

router = NestedDefaultRouter()
# quizzes_router = router.register(r'quizzes', views.QuizView, basename='quiz')
# quizzes_router.register('questions', views.QuestionView,
#                         basename='question', parents_query_lookups=['quiz'])

urlpatterns = [
    path('quizzes/', views.QuizListView.as_view()),
    path('quizzes/drafts/', views.QuizDraftsView.as_view()),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view()),
    path('quizzes/<int:pk>/questions/', views.QuestionsListView.as_view()),
    path('quizzes/<int:pk>/publish/', views.QuizPublishView.as_view()),
    path('quizzes/<int:pk>/unpublish/', views.QuizUnpublishView.as_view()),
    path('quizzes/<int:pk>/image/', views.QuizImageView.as_view()),
    path('quizzes/<int:quiz_pk>/questions/<int:question_pk>/', views.QuestionDetailView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
