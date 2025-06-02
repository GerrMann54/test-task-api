from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticleCreateView.as_view(), name='article-create'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
]
