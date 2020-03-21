from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from quiz import views
from quiz.router import NestedDefaultRouter

router = NestedDefaultRouter()

urlpatterns = [
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    path('quizzes/drafts/', views.QuizDraftsView.as_view(), name='quiz_drafts'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/<int:pk>/questions/', views.QuestionsListView.as_view(), name='questtion_list'),
    path('quizzes/<int:pk>/publish/', views.QuizPublishView.as_view(), name='quiz_publish'),
    path('quizzes/<int:pk>/unpublish/', views.QuizUnpublishView.as_view(), name='quiz_unpublish'),
    path('quizzes/<int:pk>/image/', views.QuizImageView.as_view(), name='quiz_image'),
    path('quizzes/<int:quiz_pk>/questions/<int:question_pk>/',
         views.QuestionDetailView.as_view(), name='question_detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
