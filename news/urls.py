from django.urls import path
from .views import *


urlpatterns = [
   path('', NewsList.as_view(), name = 'news_list'), 
   path('<int:pk>', PostDetail.as_view()),
   path('search/', PostSearch.as_view()),
   path('news/create/', NewsCreateView.as_view()),
   path('articles/create/', ArticleCreateView.as_view()),
   path('news/<int:pk>/edit', NewsEditView.as_view()),
   path('articles/<int:pk>/edit', ArticleEditView.as_view()),
   path('news/<int:pk>/delete', PostDelete.as_view()),
   path('articles/<int:pk>/delete', PostDelete.as_view()),
]