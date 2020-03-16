from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from quiz import views


router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
