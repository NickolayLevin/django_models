from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me

urlpatterns = [
   path('', NewsList.as_view(), name = 'news_list'), 
   path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('search/', PostSearch.as_view()),
   path('news/create/', NewsCreateView.as_view()),
   path('articles/create/', ArticleCreateView.as_view()),
   path('news/<int:pk>/edit', NewsEditView.as_view()),
   path('articles/<int:pk>/edit', ArticleEditView.as_view()),
   path('news/<int:pk>/delete', PostDelete.as_view()),
   path('articles/<int:pk>/delete', PostDelete.as_view()),
   path('news/<int:pk>/delete', PostDelete.as_view()),
   path('login/', LoginView.as_view(template_name = 'login.html'),
         name='login'),
   path('logout/', LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
   path('signup/', 
         BaseRegisterView.as_view(template_name = 'signup.html'), 
         name='signup'),
    path('news/upgrade/', upgrade_me, name = 'upgrade'),
    path('category/<int:category_id>/', CategoryNewsList.as_view(), name='news_list_by_category'),
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]
