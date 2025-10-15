from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from .models import Post, Category
from datetime import datetime
from .filters import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .tasks import *
from django.http import HttpResponse
from django.views import View
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if category.subscribers.filter(pk=request.user.pk).exists():
        category.subscribers.remove(request.user)  # Отписка
    else:
        category.subscribers.add(request.user)  # Подписка
    return redirect('news_list_by_category', category_id=category_id)


class NewsList(ListView):
 
    model = Post

    ordering = '-date'

    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostDetail(DetailView):
    
    model = Post
    
    template_name = 'post.html'
   
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
class NewsCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.PostType.NEWS
        post.save()
        form.save_m2m()
        new_post_in_category_email.delay(post_id = post.id)
        return super().form_valid(form)
        


    
    
    

class ArticleCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.PostType.ARTICLE
        post.save()
        form.save_m2m()
        return super().form_valid(form)
    

class NewsEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

class ArticleEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('news_list')

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/posts')


class CategoryNewsList(ListView):
    model = Post
    template_name = 'category_news.html'  
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return Post.objects.filter(categories=self.category, post_type=Post.PostType.NEWS).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['is_subscribed'] = self.category.subscribers.filter(pk=self.request.user.pk).exists() if self.request.user.is_authenticated else False
        return context
    
class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')