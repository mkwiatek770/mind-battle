from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from user import views


urlpatterns = [
    path('auth/create-account/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh'),
    # path('auth/login/', views.LoginView.as_view(), name='login'),
    # path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    # path('auth/refresh_token', views.RefreshTokenView.as_view(), 'refresh_token'),

    path('quizzes/<int:pk>/start/', views.QuizUserStartView.as_view(), name='quiz_start'),
    path('quizzes/<int:pk>/finish/', views.QuizUserFinishView.as_view(), name='quiz_finish'),
    path('quizzes/<int:quiz_pk>/questions/<int:question_pk>/answer/',
         views.QuestionUserAnswerView.as_view(), name='question_answer'),
    path('quizzes/<int:pk>/answer/', views.UserAnswer.as_view(), name="user_answer"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
